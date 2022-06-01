let navb = document.getElementById("top3");
let topnav=document.getElementById("top1");
function myfunction(){
    if (window.pageYOffset >=120) {
        topnav.classList.add("topscroll");
        navb.classList.add("navbarscroll");
        }
    else {
        topnav.classList.remove("topscroll");
        navb.classList.remove("navbarscroll");
        }
}
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
};