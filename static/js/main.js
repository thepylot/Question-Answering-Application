function searchToggle(obj, evt){
    var container = $(obj).closest('.search-wrapper');

    if(!container.hasClass('active')){
            container.addClass('active');
            evt.preventDefault();
    }
    else if(container.hasClass('active') && $(obj).closest('.input-holder').length == 0){
            container.removeClass('active');
            // clear input
            container.find('.search-input').val('');
            // clear and hide result container when we press close
            container.find('.result-container').fadeOut(100, function(){$(this).empty();});
    }
}

function submitFn(obj, evt){
          
    $.ajax({
            type:'POST',
            url:'/',
            data:{
              question:$('#question').val(), // get value inside the search input
              csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(json){
            // get response from views as a json
            // console.log(json)
            $(obj).find('.result-container').html('<span>Answer: ' + json.answer + '</span>');
            $(obj).find('.result-container').fadeIn(100);
            
        
            },
            error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            console.log($('#total').text())
        }
    });

    evt.preventDefault();
}