// Source: https://www.jqueryscript.net/other/bootstrap-tabs-carousel.html



function bootstrapTabControl(){
  var i, items = $('.nav-link'), pane = $('.tab-pane');
//  console.log(i)
//  console.log(items)
  // next
  $('.nexttab').on('click', function(){
      for(i = 0; i < items.length; i++){
          if($(items[i]).hasClass('active') == true){
              break;
          }
      }
      if(i < items.length - 1){
          // for tab
          $(items[i]).removeClass('active');
          $(items[i+1]).addClass('active');
          // for pane
          $(pane[i]).removeClass('show active');
          $(pane[i+1]).addClass('show active');
      }

  });
  // Prev
  $('.prevtab').on('click', function(){
      for(i = 0; i < items.length; i++){
          if($(items[i]).hasClass('active') == true){
              break;
          }
      }
      if(i != 0){
          // for tab
          $(items[i]).removeClass('active');
          $(items[i-1]).addClass('active');
          // for pane
          $(pane[i]).removeClass('show active');
          $(pane[i-1]).addClass('show active');
      }
  });
}
bootstrapTabControl();


function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

var table1_tries=3;
var table2_tries=3;
var table3_tries=3;

function myAnswer(id) {
//x = document.getElementById("ans").value;
option = 0
console.log(id)

switch (id){
case "button1_table":
    x = document.getElementById("ans1").value;
    option = 1
    para = document.getElementById("para1")
    break;
  case "button2_table":
    x = document.getElementById("ans2").value;
    option = 2
    para = document.getElementById("para2")
    break;
  case "button3_table":
    x = document.getElementById("ans3").value;
    option = 3
    para = document.getElementById("para3")
    break;
}
var a = 0;

  var testInput = x;
  var num_of_zero = js_vars.sum;
//  let num_of_zero = {{ subsession.my_table|json }};
  if (testInput == String(150-num_of_zero))
  {
    para.innerHTML = "Correct Answer!";
  }
  else{
    breakeme1: if (option == 1)
    {
        if (table1_tries == 0)
        {
            break breakeme1;
        }
        if (table1_tries == 2)
        {
            $(".button1_table").click(function(){
              $(this).hide();
            });
        }
    table1_tries -= 1
    a = table1_tries
    }



    breakeme2: if (option == 2)
    {
        if (table2_tries == 0)
        {
            break breakeme2;
        }
        if (table2_tries == 2)
        {
            $(".button2_table").click(function(){
              $(this).hide();
            });
        }
    table2_tries -= 1
    a = table2_tries
    }


    breakeme3: if (option == 3)
    {
        if (table3_tries == 0)
        {
            break breakeme3;
        }
        if (table3_tries == 2)
        {
            $(".button3_table").click(function(){
              $(this).hide();
            });
        }
    table3_tries -= 1
    a = table3_tries
    }
    para.innerHTML = "Sorry, The answer is incorrect. You have " + String(a)+ " tries left";
//    throw "Sorry, The answer is incorrect. You have ${a} tries left";
  }


}