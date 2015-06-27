
function search_header() {
    if( $(".jumbotron .jumbotron_toggle i").hasClass("icon-chevron-down") ) {
        $(".jumbotron .jumbotron_text").removeClass("remove");
        $(".jumbotron .jumbotron_toggle i").removeClass("icon-chevron-down");
        $(".jumbotron .jumbotron_toggle i").addClass("icon-chevron-up");
    } else {
        $(".jumbotron .jumbotron_text").addClass("remove");
        $(".jumbotron .jumbotron_toggle i").removeClass("icon-chevron-up");
        $(".jumbotron .jumbotron_toggle i").addClass("icon-chevron-down");
    }
}
