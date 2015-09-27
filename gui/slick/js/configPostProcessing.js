$(document).ready(function () {
    // http://stackoverflow.com/questions/2219924/idiomatic-jquery-delayed-event-only-after-a-short-pause-in-typing-e-g-timew
    var typewatch = (function () {
        var timer = 0;
        return function (callback, ms) {
            clearTimeout(timer);
            timer = setTimeout(callback, ms);
        };
    })();

    function israr_supported() {
        var pattern = $('#naming_pattern').val();
        $.get(sbRoot + '/config/postProcessing/isRarSupported', function (data) {
            if (data !== "supported") {
                $('#unpack').qtip('option', {
                    'content.text': 'Unrar Executable not found.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-red'
                });
                $('#unpack').qtip('toggle', true);
                $('#unpack').css('background-color', '#FFFFDD');
            }
        });
    }

    function fill_examples() {
        var pattern = $('#naming_pattern').val();
        var multi = $('#naming_multi_ep :selected').val();
        var anime_type = $('input[name="naming_anime"]:checked').val();

        $.get(sbRoot + '/config/postProcessing/testNaming', {pattern: pattern, anime_type: 3}, function (data) {
            if (data) {
                $('#naming_example').text(data + '.ext');
                $('#naming_example_div').show();
            } else {
                $('#naming_example_div').hide();
            }
        });

        $.get(sbRoot + '/config/postProcessing/testNaming', {pattern: pattern, multi: multi, anime_type: 3}, function (data) {
            if (data) {
                $('#naming_example_multi').text(data + '.ext');
                $('#naming_example_multi_div').show();
            } else {
                $('#naming_example_multi_div').hide();
            }
        });

        $.get(sbRoot + '/config/postProcessing/isNamingValid', {pattern: pattern, multi: multi, anime_type: anime_type}, function (data) {
            if (data == "invalid") {
                $('#naming_pattern').qtip('option', {
                    'content.text': 'This pattern is invalid.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-red'
                });
                $('#naming_pattern').qtip('toggle', true);
                $('#naming_pattern').css('background-color', '#FFDDDD');
            } else if (data == "seasonfolders") {
                $('#naming_pattern').qtip('option', {
                    'content.text': 'This pattern would be invalid without the folders, using it will force "Flatten" off for all shows.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-red'
                });
                $('#naming_pattern').qtip('toggle', true);
                $('#naming_pattern').css('background-color', '#FFFFDD');
            } else {
                $('#naming_pattern').qtip('option', {
                    'content.text': 'This pattern is valid.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-green'
                });
                $('#naming_pattern').qtip('toggle', false);
                $('#naming_pattern').css('background-color', '#FFFFFF');
            }
        });
    }

    function fill_abd_examples() {
        var pattern = $('#naming_abd_pattern').val();

        $.get(sbRoot + '/config/postProcessing/testNaming', {pattern: pattern, abd: 'True'}, function (data) {
            if (data) {
                $('#naming_abd_example').text(data + '.ext');
                $('#naming_abd_example_div').show();
            } else {
                $('#naming_abd_example_div').hide();
            }
        });

        $.get(sbRoot + '/config/postProcessing/isNamingValid', {pattern: pattern, abd: 'True'}, function (data) {
            if (data == "invalid") {
                $('#naming_abd_pattern').qtip('option', {
                    'content.text': 'This pattern is invalid.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-red'
                });
                $('#naming_abd_pattern').qtip('toggle', true);
                $('#naming_abd_pattern').css('background-color', '#FFDDDD');
            } else if (data == "seasonfolders") {
                $('#naming_abd_pattern').qtip('option', {
                    'content.text': 'This pattern would be invalid without the folders, using it will force "Flatten" off for all shows.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-red'
                });
                $('#naming_abd_pattern').qtip('toggle', true);
                $('#naming_abd_pattern').css('background-color', '#FFFFDD');
            } else {
                $('#naming_abd_pattern').qtip('option', {
                    'content.text': 'This pattern is valid.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-green'
                });
                $('#naming_abd_pattern').qtip('toggle', false);
                $('#naming_abd_pattern').css('background-color', '#FFFFFF');
            }
        });
    }

    function fill_sports_examples() {
        var pattern = $('#naming_sports_pattern').val();

        $.get(sbRoot + '/config/postProcessing/testNaming', {pattern: pattern, sports: 'True'}, function (data) {
            if (data) {
                $('#naming_sports_example').text(data + '.ext');
                $('#naming_sports_example_div').show();
            } else {
                $('#naming_sports_example_div').hide();
            }
        });

        $.get(sbRoot + '/config/postProcessing/isNamingValid', {pattern: pattern, sports: 'True'}, function (data) {
            if (data == "invalid") {
                $('#naming_sports_pattern').qtip('option', {
                    'content.text': 'This pattern is invalid.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-red'
                });
                $('#naming_sports_pattern').qtip('toggle', true);
                $('#naming_sports_pattern').css('background-color', '#FFDDDD');
            } else if (data == "seasonfolders") {
                $('#naming_sports_pattern').qtip('option', {
                    'content.text': 'This pattern would be invalid without the folders, using it will force "Flatten" off for all shows.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-red'
                });
                $('#naming_sports_pattern').qtip('toggle', true);
                $('#naming_sports_pattern').css('background-color', '#FFFFDD');
            } else {
                $('#naming_sports_pattern').qtip('option', {
                    'content.text': 'This pattern is valid.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-green'
                });
                $('#naming_sports_pattern').qtip('toggle', false);
                $('#naming_sports_pattern').css('background-color', '#FFFFFF');
            }
        });
    }

    function fill_anime_examples() {
        var pattern = $('#naming_anime_pattern').val();
        var multi = $('#naming_anime_multi_ep :selected').val();
        var anime_type = $('input[name="naming_anime"]:checked').val();

        $.get(sbRoot + '/config/postProcessing/testNaming', {pattern: pattern, anime_type: anime_type}, function (data) {
            if (data) {
                $('#naming_example_anime').text(data + '.ext');
                $('#naming_example_anime_div').show();
            } else {
                $('#naming_example_anime_div').hide();
            }
        });

        $.get(sbRoot + '/config/postProcessing/testNaming', {pattern: pattern, multi: multi, anime_type: anime_type}, function (data) {
            if (data) {
                $('#naming_example_multi_anime').text(data + '.ext');
                $('#naming_example_multi_anime_div').show();
            } else {
                $('#naming_example_multi_anime_div').hide();
            }
        });

        $.get(sbRoot + '/config/postProcessing/isNamingValid', {pattern: pattern, multi: multi, anime_type: anime_type}, function (data) {
            if (data == "invalid") {
                $('#naming_pattern').qtip('option', {
                    'content.text': 'This pattern is invalid.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-red'
                });
                $('#naming_pattern').qtip('toggle', true);
                $('#naming_pattern').css('background-color', '#FFDDDD');
            } else if (data == "seasonfolders") {
                $('#naming_pattern').qtip('option', {
                    'content.text': 'This pattern would be invalid without the folders, using it will force "Flatten" off for all shows.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-red'
                });
                $('#naming_pattern').qtip('toggle', true);
                $('#naming_pattern').css('background-color', '#FFFFDD');
            } else {
                $('#naming_pattern').qtip('option', {
                    'content.text': 'This pattern is valid.',
                    'style.classes': 'qtip-rounded qtip-shadow qtip-green'
                });
                $('#naming_pattern').qtip('toggle', false);
                $('#naming_pattern').css('background-color', '#FFFFFF');
            }
        });
    }

    function setup_naming() {
        // if it is a custom selection then show the text box
        if ($('#name_presets :selected').val() == "Custom...") {
            $('#naming_custom').show();
        } else {
            $('#naming_custom').hide();
            $('#naming_pattern').val($('#name_presets :selected').attr('id'));
        }
        fill_examples();
    }

    function setup_abd_naming() {
        // if it is a custom selection then show the text box
        if ($('#name_abd_presets :selected').val() == "Custom...") {
            $('#naming_abd_custom').show();
        } else {
            $('#naming_abd_custom').hide();
            $('#naming_abd_pattern').val($('#name_abd_presets :selected').attr('id'));
        }
        fill_abd_examples();
    }

    function setup_sports_naming() {
        // if it is a custom selection then show the text box
        if ($('#name_sports_presets :selected').val() == "Custom...") {
            $('#naming_sports_custom').show();
        } else {
            $('#naming_sports_custom').hide();
            $('#naming_sports_pattern').val($('#name_sports_presets :selected').attr('id'));
        }
        fill_sports_examples();
    }

    function setup_anime_naming() {
        // if it is a custom selection then show the text box
        if ($('#name_anime_presets :selected').val() == "Custom...") {
            $('#naming_anime_custom').show();
        } else {
            $('#naming_anime_custom').hide();
            $('#naming_anime_pattern').val($('#name_anime_presets :selected').attr('id'));
        }
        fill_anime_examples();
    }

    $('#unpack').on('change', function(){
        if(this.checked) {
            israr_supported();
        } else {
            $('#unpack').qtip('toggle', false);
        }
    });

    $('#name_presets').on('change', function(){
        setup_naming();
    });

    $('#name_abd_presets').on('change', function(){
        setup_abd_naming();
    });

    $('#naming_custom_abd').on('change', function(){
        setup_abd_naming();
    });

    $('#name_sports_presets').on('change', function(){
        setup_sports_naming();
    });

    $('#naming_custom_sports').on('change', function(){
        setup_sports_naming();
    });

    $('#name_anime_presets').on('change', function(){
        setup_anime_naming();
    });

    $('#naming_custom_anime').on('change', function(){
        setup_anime_naming();
    });

    $('input[name="naming_anime"]').on('click', function(){
        setup_anime_naming();
    });

    $('#naming_multi_ep').change(fill_examples);
    $('#naming_pattern').focusout(fill_examples);
    $('#naming_pattern').keyup(function () {
        typewatch(function () {
            fill_examples();
        }, 500);
    });

    $('#naming_anime_multi_ep').change(fill_anime_examples);
    $('#naming_anime_pattern').focusout(fill_anime_examples);
    $('#naming_anime_pattern').keyup(function () {
        typewatch(function () {
            fill_anime_examples();
        }, 500);
    });

    $('#naming_abd_pattern').focusout(fill_examples);
    $('#naming_abd_pattern').keyup(function () {
        typewatch(function () {
            fill_abd_examples();
        }, 500);
    });

    $('#naming_sports_pattern').focusout(fill_examples);
    $('#naming_sports_pattern').keyup(function () {
        typewatch(function () {
            fill_sports_examples();
        }, 500);
    });

    $('#naming_anime_pattern').focusout(fill_examples);
    $('#naming_anime_pattern').keyup(function () {
        typewatch(function () {
            fill_anime_examples();
        }, 500);
    });

    $('#show_naming_key').on('click', function(){
        $('#naming_key').toggle();
    });
    $('#show_naming_abd_key').on('click', function(){
        $('#naming_abd_key').toggle();
    });
    $('#show_naming_sports_key').on('click', function(){
        $('#naming_sports_key').toggle();
    });
    $('#show_naming_anime_key').on('click', function(){
        $('#naming_anime_key').toggle();
    });
    $('#do_custom').on('click', function(){
        $('#naming_pattern').val($('#name_presets :selected').attr('id'));
        $('#naming_custom').show();
        $('#naming_pattern').focus();
    });
    setup_naming();
    setup_abd_naming();
    setup_sports_naming();
    setup_anime_naming();

    // -- start of metadata options div toggle code --
    $('#metadataType').on('change keyup', function () {
        $(this).showHideMetadata();
    });

    $.fn.showHideMetadata = function () {
        $('.metadataDiv').each(function () {
            var targetName = $(this).attr('id');
            var selectedTarget = $('#metadataType :selected').val();

            if (selectedTarget == targetName) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    };
    //initialize to show the div
    $(this).showHideMetadata();
    // -- end of metadata options div toggle code --

    $('.metadata_checkbox').on('click', function(){
        $(this).refreshMetadataConfig(false);
    });

    $.fn.refreshMetadataConfig = function (first) {
        var cur_most = 0;
        var cur_most_provider = '';

        $('.metadataDiv').each(function () {
            var generator_name = $(this).attr('id');

            var config_arr = [];
            var show_metadata = $("#" + generator_name + "_show_metadata").prop('checked');
            var episode_metadata = $("#" + generator_name + "_episode_metadata").prop('checked');
            var fanart = $("#" + generator_name + "_fanart").prop('checked');
            var poster = $("#" + generator_name + "_poster").prop('checked');
            var banner = $("#" + generator_name + "_banner").prop('checked');
            var episode_thumbnails = $("#" + generator_name + "_episode_thumbnails").prop('checked');
            var season_posters = $("#" + generator_name + "_season_posters").prop('checked');
            var season_banners = $("#" + generator_name + "_season_banners").prop('checked');
            var season_all_poster = $("#" + generator_name + "_season_all_poster").prop('checked');
            var season_all_banner = $("#" + generator_name + "_season_all_banner").prop('checked');

            config_arr.push(show_metadata ? '1' : '0');
            config_arr.push(episode_metadata ? '1' : '0');
            config_arr.push(fanart ? '1' : '0');
            config_arr.push(poster ? '1' : '0');
            config_arr.push(banner ? '1' : '0');
            config_arr.push(episode_thumbnails ? '1' : '0');
            config_arr.push(season_posters ? '1' : '0');
            config_arr.push(season_banners ? '1' : '0');
            config_arr.push(season_all_poster ? '1' : '0');
            config_arr.push(season_all_banner ? '1' : '0');

            var cur_num = 0;
            for (var i = 0; i < config_arr.length; i++) {
                cur_num += parseInt(config_arr[i]);
            }
            if (cur_num > cur_most) {
                cur_most = cur_num;
                cur_most_provider = generator_name;
            }

            $("#" + generator_name + "_eg_show_metadata").attr('class', show_metadata ? 'enabled' : 'disabled');
            $("#" + generator_name + "_eg_episode_metadata").attr('class', episode_metadata ? 'enabled' : 'disabled');
            $("#" + generator_name + "_eg_fanart").attr('class', fanart ? 'enabled' : 'disabled');
            $("#" + generator_name + "_eg_poster").attr('class', poster ? 'enabled' : 'disabled');
            $("#" + generator_name + "_eg_banner").attr('class', banner ? 'enabled' : 'disabled');
            $("#" + generator_name + "_eg_episode_thumbnails").attr('class', episode_thumbnails ? 'enabled' : 'disabled');
            $("#" + generator_name + "_eg_season_posters").attr('class', season_posters ? 'enabled' : 'disabled');
            $("#" + generator_name + "_eg_season_banners").attr('class', season_banners ? 'enabled' : 'disabled');
            $("#" + generator_name + "_eg_season_all_poster").attr('class', season_all_poster ? 'enabled' : 'disabled');
            $("#" + generator_name + "_eg_season_all_banner").attr('class', season_all_banner ? 'enabled' : 'disabled');
            $("#" + generator_name + "_data").val(config_arr.join('|'));

        });

        if (cur_most_provider !== '' && first) {
            $('#metadataType option[value=' + cur_most_provider + ']').attr('selected', 'selected');
            $(this).showHideMetadata();
        }
    };

    $(this).refreshMetadataConfig(true);
    $('img[title]').qtip({
        position: {
            viewport: $(window),
            at: 'bottom center',
            my: 'top right'
        },
        style: {
            tip: {
                corner: true,
                method: 'polygon'
            },
            classes: 'qtip-shadow qtip-dark'
        }
    });
    $('i[title]').qtip({
        position: {
            viewport: $(window),
            at: 'top center',
            my: 'bottom center'
        },
        style: {
            tip: {
                corner: true,
                method: 'polygon'
            },
            classes: 'qtip-rounded qtip-shadow ui-tooltip-sb'
        }
    });
    $('.custom-pattern,#unpack').qtip({
        content: 'validating...',
        show: {
            event: false,
            ready: false
        },
        hide: false,
        position: {
            viewport: $(window),
            at: 'center left',
            my: 'center right'
        },
        style: {
            tip: {
                corner: true,
                method: 'polygon'
            },
            classes: 'qtip-rounded qtip-shadow qtip-red'
        }
    });
});
