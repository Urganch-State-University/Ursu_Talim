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

