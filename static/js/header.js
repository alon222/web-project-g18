function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
      x.className += " responsive";
    } else {
      x.className = "topnav";
    }
  }
console.log("im here")
// first slider javascript


    document.addEventListener('DOMContentLoaded', function () {
        const ele = document.getElementById('wrapper1');
        // ele.style.cursor = 'grab';

        let pos = { top: 0, left: 0, x: 0, y: 0 };

        const mouseDownHandler = function (e) {
            ele.style.cursor = 'grabbing';
            ele.style.userSelect = 'none';

            pos = {
                left: ele.scrollLeft,
                top: ele.scrollTop,
                // Get the current mouse position
                x: e.clientX,
                y: e.clientY,
            };

            document.addEventListener('mousemove', mouseMoveHandler);
            document.addEventListener('mouseup', mouseUpHandler);
        };

        const mouseMoveHandler = function (e) {
            // How far the mouse has been moved
            const dx = e.clientX - pos.x;
            const dy = e.clientY - pos.y;

            // Scroll the element
            ele.scrollTop = pos.top - dy;
            ele.scrollLeft = pos.left - dx;
        };

        const mouseUpHandler = function () {
            ele.style.cursor = 'grab';
            ele.style.removeProperty('user-select');

            document.removeEventListener('mousemove', mouseMoveHandler);
            document.removeEventListener('mouseup', mouseUpHandler);
        };

        // Attach the handler
        ele.addEventListener('mousedown', mouseDownHandler);
     });
    //   popup trigger

    function openModal(){
      var modal = document.getElementById("modal");
      modal.style.display="block"
    }
    function closemodal(){
      var modal = document.getElementById("modal");
      modal.style.display="none"
    }
    function additem(){
      var item = document.getElementById("additem");
      item.style.display="block"
    }
    function closeadditem(){
      var item = document.getElementById("additem");
      item.style.display="none"
    }

    //   popup trigger

    function openModal(){
      var modal = document.getElementById("modal");
      modal.style.display="block"
    }
    function closemodal(){
      var modal = document.getElementById("modal");
      modal.style.display="none"
    }
    function additem(){
      var item = document.getElementById("additem");
      item.style.display="block"
    }
    function closeadditem(){
      var item = document.getElementById("additem");
      item.style.display="none"
    }