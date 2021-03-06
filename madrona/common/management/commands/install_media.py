from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option
import os
import sys
import glob
import shutil
try:
    set
except NameError:
    from sets import Set as set # Python 2.3 fallback

class Command(BaseCommand):
    media_dirs = ['media']
    ignore_apps = ['django.contrib.admin']
    exclude = ['CVS', '.*', '*~']
    option_list = BaseCommand.option_list + (
        make_option('--media-root', default=settings.MEDIA_ROOT, dest='media_root', metavar='DIR',
            help="Specifies the root directory in which to collect media files."),
        make_option('-n', '--dry-run', action='store_true', dest='dry_run',
            help="Do everything except modify the filesystem."),
        make_option('-a', '--admin', action='store_true', dest='admin',
            help="Include django.contrib.admin static media files."),
        make_option('-d', '--dir', action='append', default=media_dirs, dest='media_dirs', metavar='NAME',
            help="Specifies the name of the media directory to look for in each app."),
        make_option('-e', '--exclude', action='append', default=exclude, dest='exclude', metavar='PATTERNS',
            help="A space-delimited list of glob-style patterns to ignore. Use multiple times to add more."),
        make_option('-f', '--force', action='store_true', dest='force_compress',
            help="Force django-compress to re-create the compressed media files."),
        make_option('-l', '--link', action='store_true', dest='link',
            help="Create a symbolic link to each file instead of copying.")
        )
    help = 'Collect media files into a single media directory.'

    def handle(self, *app_labels, **options):
        self.dry_run = options.get('dry_run', False)
        self.include_admin = options.get('admin', False)
        self.media_root = options.get('media_root', settings.MEDIA_ROOT)
        self.force_compress = options.get('force_compress', False)

        madrona_media_dir = self.get_madrona_dir()
        project_media_dir = self.get_project_dir()
        admin_media_dir = self.get_admin_dir()

        if self.dry_run:
            print "    DRY RUN! NO FILES WILL BE MODIFIED."

        if os.path.abspath(os.path.realpath(madrona_media_dir)) == os.path.abspath(os.path.realpath(self.media_root)) or \
           os.path.abspath(os.path.realpath(project_media_dir)) == os.path.abspath(os.path.realpath(self.media_root)):
            raise Exception("Your MEDIA_ROOT setting has to be a directory other than your madrona or project media folder!")

        if self.include_admin:
            self.copy_media_to_root(admin_media_dir)
        self.copy_media_to_root(madrona_media_dir)
        self.copy_media_to_root(project_media_dir)

        self.compile_media()

        self.remove_uncompressed_media()

        self.change_mediaroot_owner()

        if settings.AWS_USE_S3_MEDIA:
            self.copy_mediaroot_to_s3()

    def get_madrona_dir(self):
        # We know madrona/media is relative to this file
        madrona_media_dir = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..','media'))
        return madrona_media_dir

    def get_project_dir(self):
        # project media may at the same level as the project base dir
        trydir = os.path.realpath(os.path.join(settings.BASE_DIR, '..', 'media'))
        if not os.path.exists(trydir):
            # ... or it may be a subdir
            trydir = os.path.realpath(os.path.join(settings.BASE_DIR, 'media'))
        projdir = trydir
        return projdir
    
    def get_admin_dir(self):
        # django admin is relative to django source
        import django
        return os.path.join(django.__path__[0], 'contrib', 'admin', 'static')

    def copy_media_to_root(self, source_dir):
        if self.dry_run:
            print "    This would copy %s to %s" % (source_dir, self.media_root)
            return

        print "    Copying %s to %s" % (source_dir, self.media_root)
        from distutils.dir_util import copy_tree
        copy_tree(source_dir, self.media_root)

        return

    def compile_media(self):
        if self.dry_run:
            print "    This would compile all the media assets in %s" % (self.media_root)
            return

        force_msg = ''
        if self.force_compress:
            force_msg = "--force"

        print "    Compiling media using synccompress %s" % force_msg
        from django.core.management import call_command
        call_command('synccompress', force=self.force_compress)
        return

    def remove_uncompressed_media(self):
        if self.dry_run:
            print "    This would remove the media assets that were alredy compiled/compressed"
            return

        print "    Removing uncompressed media (not yet implemented)"
        return

    def change_mediaroot_owner(self):
        if self.dry_run:
            print "    This would change the ownership of MEDIA_ROOT to the WSGI_USER"
            return

        if settings.WSGI_USER:
            print "    Changing %s ownership to user '%s'" % (self.media_root, settings.WSGI_USER)

            try:
                from pwd import getpwnam  
                uid = getpwnam(settings.WSGI_USER)[2]
            except KeyError:
                print "    **** WARNING: UID for user %s can't be found; %s ownership not changing" % \
                        (settings.WSGI_USER, self.media_root)
                return

            try:
                os.chown(self.media_root, uid, -1)
                for root, dirs, files in os.walk(self.media_root):  
                    for m in dirs:  
                        os.chown(os.path.join(root, m), uid, -1)
                    for m in files:
                        os.chown(os.path.join(root, m), uid, -1)
            except OSError:
                print "    **** WARNING: You don't have the permissions to change ownership of %s" % self.media_root
                print "    ****    Perhaps try running the install_media command as root?"
                print "    **** OR"
                print "    ****    Try 'sudo chown -R %s %s'" % (settings.WSGI_USER, self.media_root)
                return

        else:
            print "    Ownership of %s not altered (WSGI_USER not set)" % (self.media_root)

    def copy_mediaroot_to_s3(self):
        if settings.AWS_USE_S3_MEDIA and \
           settings.AWS_MEDIA_BUCKET and \
           settings.AWS_ACCESS_KEY and \
           settings.AWS_SECRET_KEY:
            pass
        else:
            print " AWS_USE_S3_MEDIA and associated settings are not found; Files will not be uploaded to S3" 
            return None

        if self.dry_run:
            print "    This would publish all the media in %s to your S3 bucket at %s and be accessible at url %s" % \
                (self.media_root, settings.AWS_MEDIA_BUCKET, settings.MEDIA_URL)
            return

        if self.media_root[-1] != '/':
            root = self.media_root + "/"
        else:
            root = self.media_root

        from madrona.common import s3

        for top, dirs, files in os.walk(root):
            for nm in files:       
                fpath = os.path.join(top, nm)
                key = fpath.replace(root,'')
                print "  -- Uploading %s to %s " % (fpath, key)
                s3.upload_to_s3(fpath, key)

        return
