
function part2Func(obj) {
table = document.getElementById("part2table");
//option = 0
contrib_id = document.getElementById("contrib_id")

//console.log(table.rows[9]);
punkt = 0
switch(obj.value){
case '100':
    punkt = 0
    break
case '80':
    punkt = 15
    break
case '72':
    punkt = 30
    break
case '65':
    punkt = 45
    break
case '60':
    punkt = 60
    break
case '55':
    punkt = 75
    break
case '51':
    punkt = 90
    break
case '47':
    punkt = 105
    break
case '43':
    punkt = 120
    break
case '40':
    punkt = 135
    break
case '37':
    punkt = 150
    break
case '34':
    punkt = 165
    break
case '31':
    punkt = 180
    break
case '28':
    punkt = 195
    break
case '25':
    punkt = 210
    break
case '22':
    punkt = 225
    break
case '20':
    punkt = 240
    break
}

contrib_id.innerHTML = "Eingesetzer Betrag in Punkten: " + punkt;
filluptable(obj.value)
document.getElementById('contribution').value = punkt;

//for (var i = 0, row; row = table.rows[i]; i++) {
//       //iterate through rows
//       //rows would be accessed using the "row" variable assigned in the for loop
//       for (var j = 0, col; col = row.cells[j]; j++) {
//         //iterate through columns
//         //columns would be accessed using the "col" variable assigned in the for loop
//         col.style.backgroundColor = "red";
//       }
//    }

function filluptable(num){
    var count = 0;
    for (var i = 9, row; row = table.rows[i]; i--) {
       //iterate through rows
       //rows would be accessed using the "row" variable assigned in the for loop
       for (var j = 9, col; col = row.cells[j]; j--) {
            col.style.backgroundColor = "white";
       }
    }
    for (var i = 9, row; row = table.rows[i]; i--) {
       //iterate through rows
       //rows would be accessed using the "row" variable assigned in the for loop
       for (var j = 9, col; col = row.cells[j]; j--) {
         //iterate through columns
         //columns would be accessed using the "col" variable assigned in the for loop
         count += 1
         col.style.backgroundColor = "red";
         if (count == num)
         {
            break;
         }
       }
       if (count == num)
         {
            break;
         }
    }
}

//
//function myFunct() {
//  confirm("Falls Sie den gewahlten Betrag einsetzen mochten, klicken Sie auf 'Weiter'. Klicken Sie auf 'Zuruck', falls Sie ihre Eingabe andern mochten.");
//}


//switch (value){
//case "":
//    x = document.getElementById("ans1").value;
//    option = 1
//    para = document.getElementById("para1")
//    break;
//  case "button2_table":
//    x = document.getElementById("ans2").value;
//    option = 2
//    para = document.getElementById("para2")
//    break;
//  case "button3_table":
//    x = document.getElementById("ans3").value;
//    option = 3
//    para = document.getElementById("para3")
//    break;
//}
//var a = 0;
//
//  var testInput = x;
//  var num_of_zero = js_vars.sum;
////  let num_of_zero = {{ subsession.my_table|json }};
//  if (testInput == String(150-num_of_zero))
//  {
//    para.innerHTML = "Correct Answer!";
//  }
//  else{
//    breakeme1: if (option == 1)
//    {
//        if (table1_tries == 0)
//        {
//            break breakeme1;
//        }
//        if (table1_tries == 2)
//        {
//            $(".button1_table").click(function(){
//              $(this).hide();
//            });
//        }
//    table1_tries -= 1
//    a = table1_tries
//    }
//
//
//
//    breakeme2: if (option == 2)
//    {
//        if (table2_tries == 0)
//        {
//            break breakeme2;
//        }
//        if (table2_tries == 2)
//        {
//            $(".button2_table").click(function(){
//              $(this).hide();
//            });
//        }
//    table2_tries -= 1
//    a = table2_tries
//    }
//
//
//    breakeme3: if (option == 3)
//    {
//        if (table3_tries == 0)
//        {
//            break breakeme3;
//        }
//        if (table3_tries == 2)
//        {
//            $(".button3_table").click(function(){
//              $(this).hide();
//            });
//        }
//    table3_tries -= 1
//    a = table3_tries
//    }
//    para.innerHTML = "Sorry, The answer is incorrect. You have " + String(a)+ " tries left";
////    throw "Sorry, The answer is incorrect. You have ${a} tries left";
//  }
//

}



//$(document).ready(function () {
//            document.querySelector('#obito').onclick = function () {
//                swal({
//            title: "Are you sure?",
//            text: "You will not be able to recover this imaginary file!",
//            type: "warning",
//            buttons: true,
//            showCancelButton: true,
//            confirmButtonClass: 'btn-danger',
//            confirmButtonText: 'Yes, delete it!',
//            cancelButtonText: "No, cancel plx!",
//            closeOnConfirm: false,
//            closeOnCancel: false
//            },
//             function (isConfirm) {
//                if (isConfirm) {
//                    swal("Deleted!", "Your imaginary file has been deleted!", "success");
//                    } else {
//                        swal("Cancelled", "Your imaginary file is safe :)", "error");
//                    }
//            });
//
//        };
//
//    });


//function myFunct() {
//           swal({
//            text: "Falls Sie den gewahlten Betrag einsetzen mochten, klicken Sie auf 'Weiter'. Klicken Sie auf 'Zuruck', falls Sie ihre Eingabe andern mochten.",
//            type: "warning",
//            buttons: ["Zuruck","Weiter"],
//            showCancelButton: true,
//            confirmButtonClass: 'btn-danger',
//            confirmButtonText: 'Yes, delete it!',
//            cancelButtonText: "No, cancel plx!",
//            closeOnConfirm: true,
//            closeOnCancel: true
//            }).then((result) => {
//                window.alert(result)
//                if (result){
//                  swal("Poof! Your imaginary file has been deleted!", {
//                      icon: "success",
//                      r = true
//                    });
//                  document.getElementById('contribution').submit();
//                }
//            });
//
//<!-var r = confirm("Falls Sie den gewahlten Betrag einsetzen mochten, klicken Sie auf 'Weiter'. Klicken Sie auf 'Zuruck', falls Sie ihre Eingabe andern mochten.");-->
//
//             if (r == true){
//                return true;
//            } else {
//                return false;
//            }
//
//        }









//
//        async function myFunct() {
//           var r = false;
//           let result = await swal({
//            text: "Falls Sie den gewahlten Betrag einsetzen mochten, klicken Sie auf 'Weiter'. Klicken Sie auf 'Zuruck', falls Sie ihre Eingabe andern mochten.",
//            type: "warning",
//            showDenyButton: true,  showCancelButton: true,
//            buttons: ['Zuruck', 'Weiter']
//            }).then((result) => {
//                window.alert(result);
//                if (result){
//                  r = true;
//                  return false;
//                }
//            });
//
//             if (r == true){
//                window.alert(r);
//                return true;
//            } else {
//            window.alert(r);
//                return false;
//            }
//
//        }