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
})