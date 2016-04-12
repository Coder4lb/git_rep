/*
DONE:
- play/pause;
- volume;
- progress bar.

TODO:
- backward/forward;
- repeat/shuffle;
- lyrics;
- playlist.
*/

var audio = document.getElementById('audio');
var progress = document.getElementById('progress');
var playpause = document.getElementById("play-pause");
var volume = document.getElementById("volume");
var image = document.getElementById("image");
var song = document.getElementById("song");
var author = document.getElementById("author");
var lyricContainer = document.getElementById('lyricContainer');
var rs = null;

var MEDIA_ROOT = "/media/";

// audio.controls = false;

audio.addEventListener('timeupdate', function() {
  	updateProgress();
  	if (!rs) return;
  	for (var i = 0, l = rs.length; i < l; i++) {
        if (audio.currentTime > rs[i][0] - 0.50 /*preload the lyric by 0.50s*/ ) {
            //single line display mode
            // that.lyricContainer.textContent = that.lyric[i][1];
            //scroll mode
            var line = document.getElementById('line-' + i),
                prevLine = document.getElementById('line-' + (i > 0 ? i - 1 : i));
            prevLine.className = '';
            //randomize the color of the current line of the lyric
            line.className = 'current-line' ;
            prevLine.style.fontWeight = '';
            line.style.fontWeight = 'bold';
            prevLine.style.fontSize = '19px';
            line.style.fontSize = '21px';
            lyricContainer.style.top = 80 - line.offsetTop + 'px';
        };
    };
}, false);

function togglePlayPause() {
   if (audio.paused || audio.ended) {
      playpause.title = "Pause";
      playpause.innerHTML = '<i class="fa fa-pause fa-3x"></i>';
      audio.play();
   } else {
      playpause.title = "Play";
      playpause.innerHTML = '<i class="fa fa-play fa-3x"></i>';
      audio.pause();
   }
}

function toggleRetweet(){
    var retweet = document.getElementById("retweet");
    if( audio.loop == true ){
      audio.loop = false;
      retweet.innerHTML = '<i class="fa fa-long-arrow-right fa-lg"></i>';
      retweet.title = "Single";
    }else{
      audio.loop = true;
      retweet.innerHTML = '<i class="fa fa-retweet fa-lg"></i>';
      retweet.title = "Retweet";
    }
}

function setVolume() {
   audio.volume = volume.value ;
}

function updateProgress() {	
	var percent = Math.floor((100 / audio.duration) * audio.currentTime);
	progress.value = percent;
	var canvas = document.getElementById('progress');
	var context = canvas.getContext('2d');
	var centerX = canvas.width / 2;
	var centerY = canvas.height / 2;
	var radius = 150;
	var circ = Math.PI * 2;
	var quart = Math.PI / 2;
	var cpercent = percent / 100; /* current percent */
	context.beginPath();
	context.arc(centerX, centerY, radius, 0, ((circ) * cpercent), false);
	context.lineWidth = 10;
	context.strokeStyle = '#26C5CB';
	context.stroke();
	if (audio.ended || audio.duration - audio.currentTime < 0.5  ) resetPlayer();
}

function choiceSong( url , img , title , singer , lyric ){
	resetPlayer();
	audio.src = MEDIA_ROOT + url;
	image.src = MEDIA_ROOT + img;
	song.innerHTML = '<a href="#">' + title + '</a>';
	author.innerHTML = '<a href="#">' + singer + '</a>';
    	
	var request = new XMLHttpRequest();
	request.open('GET', 'media/'+lyric , true );
	request.responseType = 'text'; //默认就是text
	//请求成功时
	request.onload = function() {
		// alert(request.responseText);
	  //responseType = 'text'情况下使用responseText拿结果
	  	if(request.responseText == 1 ){
        	lyricContainer.textContent = '读取歌词失败 :(';		
	  		return ;
	  	}
	  	rs = parseLyric(request.responseText);
	  	appendLyric(rs);
	  // console.log(request.response);
	};
	
	lyricContainer.textContent = '正在读取歌词……';
	//发送请求
	request.send();
	
	togglePlayPause();
}

function resetPlayer() {
	var canvas = document.getElementById('progress');
	var context = canvas.getContext('2d');
	audio.currentTime = 0; 
  context.clearRect(0,0,canvas.width,canvas.height);
  if( audio.loop == false){
    playpause.title = "Play";
    playpause.innerHTML = '<i class="fa fa-play fa-3x"></i>';
  }
}

function parseLyric(text) {
  var lines = text.split('\n'),
  pattern =  /\[\d{2}:\d{2}\.\d{2}\]/g;
	var result = [];

  /* 去掉不含时间的无用行 */
	 for( i=0;i<lines.length; ){
      var time = lines[i].match(pattern);
      if(time === null){
        lines.splice(i,1);
      }else i++;
   }

	lines.forEach(function(v /*数组元素值*/ , i /*元素索引*/ , a /*数组本身*/ ) {
        //提取出时间[xx:xx.xx]
        time = v.match(pattern);
       // console.log( v , time );
            //提取歌词
        var value = v.replace(pattern, '');
        //因为一行里面可能有多个时间，所以time有可能是[xx:xx.xx][xx:xx.xx][xx:xx.xx]的形式，需要进一步分隔
        time.forEach(function(v1, i1, a1) {
            //去掉时间里的中括号得到xx:xx.xx
            if(v1 !== null ){
            	var t = v1.slice(1, -1).split(':');
            }
            //将结果压入最终数组
            result.push([parseInt(t[0], 10) * 60 + parseFloat(t[1]), value]);
        });
    });
   //最后将结果数组中的元素按时间大小排序，以便保存之后正常显示歌词
    result.sort(function(a, b) {
        return a[0] - b[0];
    });
    return result;
}	

function appendLyric(lyric) {
    fragment = document.createDocumentFragment();
    //clear the lyric container first
    lyricContainer.innerHTML = '';
    lyric.forEach(function(v, i, a) {
        var line = document.createElement('p');
        line.id = 'line-' + i;
        line.textContent = v[1];
        fragment.appendChild(line);
    });
    lyricContainer.appendChild(fragment);
}