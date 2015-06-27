// NOT COMPLETE
function like_handler(event, itemname) {
    
    var item_id = $(this).attr('id').replace("like_","").replace("un",""); // the image's id
    var text=$(this).attr('id').replace(item_id,""); // current status of button : liked/not-liked

    if (text == "like_") {
        $(this).text("unlike "); // change text
        $(this).attr('id', 'unlike_' + item_id) // change id (for next time)
        $(this).attr('data-content', "HAHA_liked") // change tooltip text
        
        var ref = this;
        arguments = {
                like : "like",
                type : itemname,
                product_id : product_id
            }
        if (itemname == "image")            argumnts += { image_id : item_id }
        else if (itemname == "makey")       argumnts += { m_id : item_id }
        else if (itemname == "image")       argumnts += { image_id : item_id }
        $.post(ajax_url, { // Tell server about the change in likes, function(data){
                if ((data) == "okay"){
                    var likes = parseInt($(ref).parent().find('.imagelikes').text());
                    likes++;
                    $(ref).parent().find('.imagelikes').text(likes);
                    alert("liked");
                } else if ((data) == "login required"){
                    alert("You are not logged in. Please login to continue");
                    like.text("like "); // reverting back
                } else {
                    alert("Something went wrong. Please refresh page.");
                    like.text("like "); // relativeerting back
                }
            }
        );
    } else if (text == "unlike_") {
        $(this).text("like "); // change text
        $(this).attr('id','like_'+image_id) // change id (for next time)
        $(this).attr('data-content', "HAHA_liked") // change tooltip text
        
        var ref = this;
        $.post(ajax_url, { like:"unlike", type:"image", image_id:image_id,product_id:product_id},function(data){
            if((data)=="okay"){
                var likes = parseInt($(ref).parent().find('.imagelikes').text());
                // alert(likes);
                likes--;
                $(ref).parent().find('.imagelikes').text(likes);
                // alert("unliked")
            } else if((data)=="login required")
                alert("You are not logged in. Please login to continue");
            else {
                alert("Something went wrong. Please refresh page.");
            }
        });
    }
}

