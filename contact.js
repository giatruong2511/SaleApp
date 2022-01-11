(function ($) {
    'use strict';

    var form = $('.contact__form'),
        message = $('.contact__msg'),
        form_data;

    // Success function
    function done_func(response) {
        message.fadeIn().removeClass('alert-danger').addClass('alert-success');
        message.text(response);
        setTimeout(function () {
            message.fadeOut();
        }, 2000);
        form.find('input:not([type="submit"]), textarea').val('');
    }

    // fail function
    function fail_func(data) {
        message.fadeIn().removeClass('alert-success').addClass('alert-success');
        message.text(data.responseText);
        setTimeout(function () {
            message.fadeOut();
        }, 2000);
    }
    
    form.submit(function (e) {
        e.preventDefault();
        form_data = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form_data
        })
        .done(done_func)
        .fail(fail_func);
    });
    
})(jQuery);

function addToNote(id, name, gioitinh, yearofbirth, address) {
    event.preventDefault();

    fetch('/api/add_to_note', {
        method: 'post',
        body: JSON.stringify({
           'id': id,
           'name': name,
           'gioitinh' : gioitinh,
           'yearofbirth' : yearofbirth,
           'address' : address,
           'ngay' : ngay
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        location.reload()
        console.info(res)
        return res.json()
    }).catch(function(err) {
        console.error(err)
    })
}

function save(){

    if (confirm('Bạn chắc chắn muốn lưu danh sách không?') == true) {
        fetch('/api/save', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code == 200)
                location.reload()
            if (data.code == 400)
                alert("Lỗi")
        }).catch(err =>  console.error(err))
    }
}
function deleteNote(pId) {
    if (confirm('Ban chac chan xoa benh nhan!!!') == true) {
        fetch(`/api/delete-note/${pId}`, {
            method: 'delete'
        }).then(res => res.json()).then(data => {
            if (data.code == 200) {
                location.reload()
                let r = document.getElementById(`p${pId}`)
                r.style.display = 'none'
            } else if (data.code == 404)
                alert(data.err_msg)
        }).catch(err => console.error(err))
    }
}