document.addEventListener('DOMContentLoaded', function () {
    init();
});

function init(){
    fetch("/php/subscribe.php?pass=gharbhegutha&action=issubscribed", {
        method: 'GET',
    }).then(response => response.text()).then(resText => {
        let btnSubscribe = document.getElementById('btnSubscribe');
        console.log(resText);
        
        if(resText == 1){
            btnSubscribe.innerText = "Unsubscribe";
            btnSubscribe.style.backgroundColor = "rgba(185, 112, 29, 0.73)";
            btnSubscribe.onclick = ()=> location.href = "/php/subscribe.php?pass=gharbhegutha&action=unsubscribe";
        }else{
            btnSubscribe.innerText = "Upgrade to Premium";
            btnSubscribe.onclick = ()=> location.href = "/php/subscribe.php?pass=gharbhegutha&action=subscribe";
        }
        
    });
}