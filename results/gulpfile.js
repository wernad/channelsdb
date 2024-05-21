const gulp = require('gulp');
const concat = require('gulp-concat');

gulp.task('merge-js', function() {
    return gulp.src([
        './ChannelsDB/js/jquery-1.12.4.js',
        './ChannelsDB/js/jquery-ui.js',
        './ChannelsDB/js/jspdf.min.js',
        './ChannelsDB/js/bootstrap.min.js',
        './ChannelsDB/js/canvas2svg.js',
        './ChannelsDB/js/datagrid.js',
        './ChannelsDB/js/Palette.js',
        './ChannelsDB/js/svg2pdf.js',
        './ChannelsDB/js/tabsConfig.js',
        './ChannelsDB/js/tooltipConfig.js',
        './ChannelsDB/js/utf8.js'
    ])
      .pipe(concat('scripts.js'))
      .pipe(gulp.dest('./ChannelsDB/js'));
  });

gulp.task('merge-css', function() {
    return gulp.src([
        './ChannelsDB/css/AglomeredParameters.css',
        './ChannelsDB/css/bootstrap.min.css',
        './ChannelsDB/css/ChannelsDescriptions.css',
        './ChannelsDB/css/datagrid.css',
        './ChannelsDB/css/DownloadReport.css',
        './ChannelsDB/css/jquery-ui.css',
        './ChannelsDB/css/LayerVizualizerStyles.css',
        './ChannelsDB/css/lining-residues.css',
        './ChannelsDB/css/PDBID.css',
        './ChannelsDB/css/style.css',
        './ChannelsDB/css/tooltips.css',
    ])
      .pipe(concat('styles.css'))
      .pipe(gulp.dest('./ChannelsDB/css'));
})