const app= document.getElementById('app');
let isloaded=false;
const toggleLoader=()=>{
    if(isloaded){
        isloaded=false;
        document.getElementById('loader').remove()
    }else{
        const container = document.getElementById('container');
        const tmp=container.innerHTML;
        container.innerHTML=`
        <div id="loader">
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto; display: block; shape-rendering: auto;" width="200px" height="200px" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
                <circle cx="50" cy="50" r="0" fill="none" stroke="#e90c59" stroke-width="2">
                <animate attributeName="r" repeatCount="indefinite" dur="1s" values="0;40" keyTimes="0;1" keySplines="0 0.2 0.8 1" calcMode="spline" begin="0s"/>
                <animate attributeName="opacity" repeatCount="indefinite" dur="1s" values="1;0" keyTimes="0;1" keySplines="0.2 0 0.8 1" calcMode="spline" begin="0s"/>
                </circle><circle cx="50" cy="50" r="0" fill="none" stroke="#06458f" stroke-width="2">
                <animate attributeName="r" repeatCount="indefinite" dur="1s" values="0;40" keyTimes="0;1" keySplines="0 0.2 0.8 1" calcMode="spline" begin="-0.5s"/>
                <animate attributeName="opacity" repeatCount="indefinite" dur="1s" values="1;0" keyTimes="0;1" keySplines="0.2 0 0.8 1" calcMode="spline" begin="-0.5s"/>
                </circle>
            </svg>
        </div>`+tmp;
        isloaded=true;
    }
}
const reloadData=()=>{
    toggleLoader();
    handler.reloadData(function(json) {
            document.getElementById('table').innerHTML=json.data.table;
            document.getElementById('header-status').innerHTML=json.data.last_modified;
            document.getElementById('footer-status').innerHTML=`Saved on :  ${json.data.last_modified}`;
            toggleLoader();
    });
}
const exportFile=(filetype)=>{
    handler.exportFile(filetype);
}
new QWebChannel(qt.webChannelTransport, function (channel) {
    window.handler = channel.objects.handler;
  });

