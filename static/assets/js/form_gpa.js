document.getElementById("subject_table").addEventListener("submit", function (event) {
    event.preventDefault();
    var submitButton = event.submitter;

    if (submitButton) {
        var buttonName = submitButton.name

        var formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {


                if (buttonName === "submit_gpa") {
                    var gpaResult = document.getElementById("gpa_result");
                    var gpaElement = document.getElementById("gpa");
                    var status = document.getElementById("status");
                    var subjectTableElement = document.getElementById("subjectTable");
                    var kreditElement = document.getElementById("kredit");

                    var gpa = data.gpa;
                    gpaElement.innerText = "GPA: " + gpa;

                    var subjectList = data.gpa_subjects_list;
                    // var tableHtml = '<table class="table">';
                    // tableHtml += '<tr><th>№</th><th>Subject</th></tr>';
                    // for (var i = 0; i < subjectList.length; i++) {
                    //     tableHtml += '<tr><td>' + (i + 1) + '</td><td>' + subjectList[i] + '</td></tr>';
                    // }
                    // tableHtml += '</table>';
                    // subjectTableElement.innerHTML = tableHtml;
                    //
                    // var kredit = data.kredit_sum;
                    // kreditElement.innerText = kredit;
                    gpaResult.style.visibility = 'visible';

                    // GPA-ni tekshirish va alert chiqarish
                    if (gpa >= 2.7) {
                        gpaResult.className = 'alert alert-success';
                    } else {
                        gpaResult.className = 'alert alert-danger';
                    }
                } else if (buttonName === "download_gpa") {


                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "download_gpa_pdf/", true);

                    var formData = new FormData(document.getElementById("subject_table"));
                    var fakultet = document.getElementById("fakultet");
                    var talim_shakli = document.getElementById("talim_shakli");
                    var qabul_yili = document.getElementById("qabul_yili");
                    var yonalish = document.getElementById("yonalish");


                    var fakultetValue = fakultet.options[fakultet.selectedIndex].innerText;
                    var talim_shakliValue = talim_shakli.options[talim_shakli.selectedIndex].innerText;
                    var qabul_yiliValue = qabul_yili.options[qabul_yili.selectedIndex].innerText;
                    var yonalishValue = yonalish.options[yonalish.selectedIndex].innerText;

                    xhr.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken"));

                    xhr.responseType = "blob";

                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4) {
                            if (xhr.status === 200) {
                                var blob = xhr.response;
                                console.log(blob);

                                var link = document.createElement("a");
                                link.href = window.URL.createObjectURL(blob);
                                var unixVaqt = Date.now()

                                var name="GPA"+""+unixVaqt+".pdf"
                                link.download = name;
                                link.style.display = "none";
                                document.body.appendChild(link);
                                link.click();
                                document.body.removeChild(link);
                            }
                        }
                    };
                    formData.append("fakultet", fakultetValue);
                    formData.append("talim_shakli", talim_shakliValue);
                    formData.append("qabul_yili", qabul_yiliValue);
                    formData.append("yonalish", yonalishValue);
                    xhr.send(formData);
                }

            })
            .catch(error => {
                console.error('Xatolik yuz berdi:', error);
            });


    }

});

document.getElementById("mainform").addEventListener("submit", function (event) {
    event.preventDefault();
    var formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            var subject_div = document.getElementById("subject_div");
            var gpaResult = document.getElementById("gpa_result");
            var subjectList = data.subjects_list;
            if (subjectList.length >= 1) {
                subject_div.style.visibility = 'visible';
                gpaResult.style.visibility = 'hidden';

                var tableHtml = '';
                var tableBody = document.getElementById("table_body") || "";

                for (var i = 0; i < subjectList.length; i++) {
                    var subject = subjectList[i];
                    if (Array.isArray(subject[0])) {
                        tableHtml += '<tr>';
                        tableHtml += '<td class="text-start">' + (i + 1) + '</td>';
                        tableHtml += '<td>';
                        for (var j = 0; j < subject.length; j++) {
                            tableHtml += subject[j][0] + '<br>';
                        }
                        tableHtml += '</td><input type="hidden" name="subject_name[]" value="' + subject[0][0] + '">';
                        tableHtml += '<td>' + subject[0][2] + '</td>';
                        tableHtml += '<td>' + subject[0][3] +'<input type="hidden" name="block[]" value="' + subject[0][3] + '"></td>';
                        tableHtml += '<td>' + subject[0][6] + '-semestr'+'<input type="hidden" name="semestr[]" value="' + subject[0][6] + '"></td>';
                        tableHtml += '<td>' + subject[0][4] + '</td>';
                        tableHtml += '<td>' + subject[0][5] + '<input type="hidden" name="credit[]" value="' + subject[0][5] + '"></td>';
                        tableHtml += '<td><input type="number" class="form-control" name="grade[]" min="0" max="5"></td>';
                        tableHtml += '</tr>';
                    } else {
                        tableHtml += '<tr>';
                        tableHtml += '<td class="text-start">' + (i + 1) + '</td>';
                        tableHtml += '<td>' + subject[0] + '<input type="hidden" name="subject_name[]" value="' + subject[0] + '"></td>';
                        tableHtml += '<td>' + subject[2] + '</td>';
                        tableHtml += '<td>' + subject[3] + '<input type="hidden" name="block[]" value="' + subject[3] + '"></td>';
                        tableHtml += '<td>' + subject[6] + '-semestr'+'<input type="hidden" name="semestr[]" value="' + subject[6] + '"></td>';
                        tableHtml += '<td>' + subject[4] + '</td>';
                        tableHtml += '<td>' + subject[5] + '<input type="hidden" name="credit[]" value="' + subject[5] + '"></td>';
                        tableHtml += '<td><input type="number" class="form-control" name="grade[]" min="0" max="5"></td>';
                        tableHtml += '</tr>';
                    }
                }

                tableBody.innerHTML = tableHtml;
            } else {
                subject_div.style.visibility = 'hidden';
            }
        })
        .catch(error => {
            console.error('Xatolik yuz berdi:', error);
        });
});
