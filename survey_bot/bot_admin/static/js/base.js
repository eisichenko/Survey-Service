$(document).ready(function() {
    var min_diff = 1e9
    var min_href = undefined

    // highlighting navigation bar
    $('a').each(function (_, cur_ref) 
    {
        cur_ref = cur_ref.href

        window_ref = window.location.href

        substr_start = window_ref.indexOf(cur_ref)

        if (substr_start >= 0)
        {
            substr_end = substr_start + cur_ref.length - 1

            cur_diff = window_ref.length - substr_end - 1
    
            if (min_diff > cur_diff && cur_diff >= 0) 
            {
                min_href = this
                min_diff = cur_diff
            }
        }
    });

    $(min_href).addClass("active");

    console.log(min_href)

    $('#download-button').click(function() {
        if ($('input[name=choices]').is(':checked')) {
            if (confirm('Downloading telegram files may take some time.\n\nAre you sure to start downloading?')){
                $('#download-div').css('display', 'block');
                $('#server-message').css('display', 'none');

                $.fileDownload($(this).prop('href'))
                    .done(function () {
                        console.log("OK");
                        $('#download-div').css('display', 'none');
                        $('#server-message').css('display', 'block');
                        $('#server-message').text('Answers were downloaded successfully!');
                        $('#server-message').css('color', '#2fbe2f');
                    })
                    .fail(function () { 
                        console.log("FAIL");
                        $('#download-div').css('display', 'none');
                        $('#server-message').css('display', 'block');
                        $('#server-message').text('Downloading answers was failed :(');
                        $('#server-message').css('color', '#f00');
                    });
            
                return true;
            }
            return false;
        }
    })
})