
function toggle_list(elem) {
    if( $('.list_toggle').hasClass("list_shown") ) {
        $('.list_toggle').removeClass("list_shown")
        $('.list_toggle').addClass("list_closed")

        $('#list_toggle_a').mouseleave( function() {
            $('#list_toggle_a i').removeClass("icon-chevron-down")
            $('#list_toggle_a i').addClass("icon-chevron-up")
        } );
        
    } else if( $('.list_toggle').hasClass("list_closed") ) {
        $('.list_toggle').removeClass("list_closed")
        $('.list_toggle').addClass("list_shown")
        $('#list_toggle_a').mouseleave( function() {
            $('#list_toggle_a i').removeClass("icon-chevron-down")
            $('#list_toggle_a i').addClass("icon-chevron-up")
        } );

        
    }
}
