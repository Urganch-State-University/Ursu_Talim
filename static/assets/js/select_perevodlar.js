document.getElementById('fakultet').addEventListener('change', function () {
    document.getElementById('talim_shakli').value = "";  // Talim shaklini tozalash
    document.getElementById('qabul_yili').value = "";    // Qabul yilini tozalash
    document.getElementById('yonalish').value = "";      // Yonalishni tozalash
    document.getElementById('semester').value = "";      // Semestrni tozalash
});


document.getElementById('talim_shakli').addEventListener('change', function () {
    document.getElementById('yonalish').value = "";  // Yonalishni tozalash
    document.getElementById('semester').value = "";  // Semestrni tozalash
});


document.getElementById('qabul_yili').addEventListener('change', function () {
    document.getElementById('yonalish').value = "";  // Yonalishni tozalash
    document.getElementById('semester').value = "";  // Semestrni tozalash

    var fakultet = document.getElementById('fakultet').value;
    var talim_shakli = document.getElementById('talim_shakli').value;
    var qabul_yili = document.getElementById('qabul_yili').value;


});

$(document).ready(function () {
    $("#qabul_yili").on("change", function () {
        var fakultet = document.getElementById("fakultet").value;
        var talim_shakli = document.getElementById("talim_shakli").value;
        var qabul_yili = $(this).val();

        // AJAX so'rovni yuborish
        $.ajax({
            url: '/ajax_get_options/', // AJAX so'rovni qabul qiladigan Django view manzili
            data: {
                'fakultet': fakultet,
                'talim_shakli': talim_shakli,
                'qabul_yili': qabul_yili,

            },
            dataType: 'json',
            success: function (data) {
                console.log(data.curriculum_list);
                // Keyingi selectni yangilash
                var yonalish = $("#yonalish");
                yonalish.empty();
                $.each(data.curriculum_list, function (key, value) {
                    yonalish.append('<option value="' + key + '">' + value + '</option>');
                });
                var semester = $("#semester");
                semester.empty();
                $.each(data.semester_list, function (key, value) {
                    semester.append('<option value="' + key + '">' + value + '</option>');
                });
            }
        });
    });
});