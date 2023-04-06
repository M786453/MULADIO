
window.onload = function(){


const submitBtn = document.getElementById('submit-btn');

const closePlayer = document.getElementById('parent-player-close');

console.log(document);

closePlayer.addEventListener('click', () => {

    document.getElementById('parent-player').style.display = 'none';

    document.getElementById('form_div').style.display = 'block';

});

submitBtn.addEventListener('click', () => {
	

    const urlInput = document.getElementById('url-input').value;
    
    const lang = document.getElementById('lang').value;
      
    const url = `http://127.0.0.1:8000/generate?url-input=${urlInput}&lang=${lang}`;

    if (urlInput === '' && lang === '') {
        
        alert('Please fill in both fields!');

      
    } else {

        submitBtn.innerHTML = 'Loading...';

        submitBtn.disabled = true;

        const xhr = new XMLHttpRequest();
        
        xhr.open('GET', url, true);

        xhr.onload = function() {
          
            if (this.status === 200) {
                console.log(this.responseText)
                submitBtn.innerHTML = 'CONVERT'
                submitBtn.disabled = false;
                if(this.responseText === 'Error Occured.'){
                    alert("Error Occured.");
                }else if(this.responseText === "URL/LANG FIELD EMPTY."){
                    alert("URL/LANG FIELD EMPTY.");
                }else if(this.responseText === "Invalid Youtube Video URL."){
                    alert("Invalid Youtube Video URL.");
                }else if(this.responseText === "Invalid Language."){
                    alert("Invalid Language.");
                }else{
                    var jsonData = JSON.parse(this.responseText);         
                    setupYtPlayer(jsonData['video_id'], jsonData['audio_length']);
                }

          
            }
        
        };

        xhr.send();
      
    }


});


}




function setupYtPlayer(id, audio_length){
   
        //   Create a new YouTube player object

        const audio = document.getElementById('audio')

        // Hide form
        document.getElementById('form_div').style.display = 'none'

        // Show Player
        document.getElementById('parent-player').style.display = 'block'

        audio.src = "../static/res/audios/target/translated_audio.mp3"

        var player = new YT.Player('player', {
                height: '100%',
                width: '100%',
                videoId: id
            });

        
            
            
        // Add an event listener for the onStateChange event
        player.addEventListener("onStateChange", function(event) {
                
            if (event.data == YT.PlayerState.PLAYING) {

                // Mute the YouTube player
                player.mute();
                    
                original_video_length = player.getDuration();

                new_video_length = original_video_length/audio_length;

                console.log(new_video_length);
                    
                player.setPlaybackRate(new_video_length);

                audio.play();

            }else{
                    
                
                audio.pause();
                
            }
                
        });

    
}
