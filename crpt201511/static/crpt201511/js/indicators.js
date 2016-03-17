
function UpdateText(sheet,place,dataFile, opt){
	console.log('Init Text:'+place+"/"+dataFile);
	var content = {linia:[]};
	
	var url = "https://spreadsheets.google.com/feeds/list/"+dataFile+"/"+sheet+"/public/values?alt=json";
	console.log('Init Text: Sheet('+sheet+') TextNum ('+place+') URL ('+url+')');

	$.getJSON(url, function(data) {
		for( var i=0;i<data.feed.entry.length;i++){
			var tmp=new Object();
			var columns=0;
			if(eval('data.feed.entry['+i+'].gsx$field1')){tmp.field1=eval('data.feed.entry['+i+'].gsx$field1.$t');columns++;};
			if(eval('data.feed.entry['+i+'].gsx$field2')){tmp.field2=eval('data.feed.entry['+i+'].gsx$field2.$t');columns++;};
			if(eval('data.feed.entry['+i+'].gsx$field3')){tmp.field3=eval('data.feed.entry['+i+'].gsx$field3.$t');columns++;};
			if(eval('data.feed.entry['+i+'].gsx$field4')){tmp.field4=eval('data.feed.entry['+i+'].gsx$field4.$t');columns++;};
			if(eval('data.feed.entry['+i+'].gsx$field5')){tmp.field5=eval('data.feed.entry['+i+'].gsx$field5.$t');columns++;};
			if(eval('data.feed.entry['+i+'].gsx$nivell')){tmp.nivell=eval('data.feed.entry['+i+'].gsx$nivell.$t');};
			if(eval('data.feed.entry['+i+'].gsx$estat')){tmp.estat=eval('data.feed.entry['+i+'].gsx$estat.$t');};
			tmp.columns=columns;
			content.linia.push(tmp);
			console.log("TEXT: "+content.linia[i-1]);
		};
		var template = $('#text-template').html();
		var info = Mustache.to_html(template, content);
		$(place).html(info);

	}); 
	console.log('end Text List');
};



function UpdateChartLines(sheet, place, dataFile, intervalY, unitatsY, labels, multiAxi){
// sheet: sheet del full de càlcul
// place: etiqueta HTML a substituir
// dataFile: GoogleDrive
// intervalY: cada quantes unitats va una divisió Y
// unitatsY: ARRAY de etiquetes per cada eix de cada SERIE ( si multiAxis=TRUE )
// labels: TRUE/FALSE si posa etiquetes o no
// multiAxi: TRUE/FALSE si es vol múltiple eix Y
	var newData;
	var valors = [];
	var Yaxis = [];
	var idx=0;
	var resultsArray = [];
	var XLabels=[];
	
	
//	var url = "https://spreadsheets.google.com/feeds/list/"+dataFile+"/od6/public/values?alt=json";
	var url = "https://spreadsheets.google.com/feeds/list/"+dataFile+"/"+sheet+"/public/values?alt=json";
	//https://spreadsheets.google.com/feeds/list/' + urlLocation + '/od6/public/values?alt=json';
	console.log('Init Chart: Sheet('+sheet+') ChartNum ('+place+') URL ('+url+')');

	$.getJSON(url, function(data) {
		for (var j=0;j<25;j++){
			var fl='data.feed.entry[0].gsx$c'+j;
			if(eval(fl)){
				XLabels.push(eval(fl+'.$t'));
			}
		}
		console.log("Categories: "+XLabels);
		for( var i=1;i<data.feed.entry.length;i++){
			var Ytmp=new Object();
			var Vtmp=new Object();
			
			Vtmp.name=eval('data.feed.entry['+i+'].gsx$serie.$t');
			if ( multiAxi ) Vtmp.yAxis=i-1;
			else Vtmp.yAxis=0;
			Vtmp.type='line';
			Ytmp.title={text : unitatsY[i-1], style: { color: colorbrewer[colorPalette][colorPick][i-1]}};
			Ytmp.id=i-1;
			Ytmp.tickInterval=intervalY;
			Ytmp.labels={format:'{value:,.0f}',style: {color: colorbrewer[colorPalette][colorPick][i-1]}};
			if ( i>1) {
				Ytmp.opposite=true;
			}
			console.log("Serie:"+Vtmp.name);
			Vtmp.data=[];
			for (var j=0;j<25;j++){
				var fl='data.feed.entry['+i+'].gsx$c'+j;
				if(eval(fl)){
					var str=eval(fl+'.$t').replace('.','');
					str=str.replace(',','.');
					if(str==''){str='0';j=25}
					else{
						Vtmp.data[j]=parseFloat( str);
						console.log(fl+'.$t = '+Vtmp.data[j]);
					};
				}
			}
			valors.push(Vtmp);
			if(multiAxi||(i==1)) { 
				Yaxis.push(Ytmp) ;
			};
			console.log(valors[i-1]);
		};

		console.log(place);
		$(place).highcharts({
			chart: {
				type: 'line',
				height:'300',
			},
			credits: {
				enabled: false
			},
			title: {
				text: data.feed.title.$t,
				style: { fontSize: titleFontSize, fontWeight: "bold", color:titleColor},
			},
			colors: colorbrewer[colorPalette][colorPick].slice(),
			xAxis: {
				categories: XLabels
			},
			yAxis: Yaxis,
			/*{
				title: {
					text: unitatsY
				},
				tickInterval: intervalY,
				labels: {
					format: '{value:,.0f}'
				}
			},*/
			plotOptions: {
				line: {
					dataLabels: {
						enabled: labels,
						allowOverlap: true,
						color: '#222222',
						style: { fontSize: '8px',textShadow: "0px 0px 5px #eeeeee", fontWeight: "normal"},
						shadow: false,
					    formatter: function() {
							if (this.y != 0) {
							  return this.y.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,")
							} else {
							  return null;
							}
						}
					}
				}
			},
			legend:{
				itemStyle: {  cursor: 'pointer', fontSize: legendFontSize, fontWeight: 'normal' }
			},
			tooltip: {
			  pointFormat: '{series.name}: <b>{point.y}</b><br/>',
			  shared: true
			},
			series: valors
		});
	});
	console.log('end config HighChart');
};




function UpdateChartSpider(sheet, place, dataFile, intervalY, unitatsY, labels, multiAxi){
// sheet: sheet del full de càlcul
// place: etiqueta HTML a substituir
// dataFile: GoogleDrive
// intervalY: cada quantes unitats va una divisió Y
// unitatsY: ARRAY de etiquetes per cada eix de cada SERIE ( si multiAxis=TRUE )
// labels: TRUE/FALSE si posa etiquetes o no
// multiAxi: TRUE/FALSE si es vol múltiple eix Y
	var newData;
	var valors = [];
	var Yaxis = [];
	var idx=0;
	var resultsArray = [];
	var XLabels=[];
	
	var url = "https://spreadsheets.google.com/feeds/list/"+dataFile+"/"+sheet+"/public/values?alt=json";
	console.log('Init Chart: Sheet('+sheet+') ChartNum ('+place+') URL ('+url+')');

	$.getJSON(url, function(data) {
		for (var j=0;j<25;j++){
			var fl='data.feed.entry[0].gsx$c'+j;
			if(eval(fl)){
				XLabels.push(eval(fl+'.$t'));
			}
		}
		console.log("Categories: "+XLabels);
		for( var i=1;i<data.feed.entry.length;i++){
			var Ytmp=new Object();
			var Vtmp=new Object();
			
			Vtmp.name=eval('data.feed.entry['+i+'].gsx$serie.$t');
			if ( multiAxi ) Vtmp.yAxis=i-1;
			else Vtmp.yAxis=0;
			Vtmp.type='line';
			Ytmp.title={text : unitatsY[i-1], style: { color: colorbrewer[colorPalette][colorPick][i-1]}};
			Ytmp.id=i-1;
			Ytmp.tickInterval=intervalY;
			Ytmp.labels={format:'{value:,.0f}',style: {color: colorbrewer[colorPalette][colorPick][i-1]}};
			if ( i>1) {
				Ytmp.opposite=true;
			}
			console.log("Serie:"+Vtmp.name);
			Vtmp.data=[];
			for (var j=0;j<25;j++){
				var fl='data.feed.entry['+i+'].gsx$c'+j;
				if(eval(fl)){
					var str=eval(fl+'.$t').replace('.','');
					str=str.replace(',','.');
					if(str==''){str='0';j=25}
					else{
						Vtmp.data[j]=parseFloat( str);
						console.log(fl+'.$t = '+Vtmp.data[j]);
					};
				}
			}
			Vtmp.pointPlacement='on';
			valors.push(Vtmp);
			if(multiAxi||(i==1)) { 
				Yaxis.push(Ytmp) ;
			};
			console.log(valors[i-1]);
		};

		console.log(place);
    
      $(place).highcharts({

        chart: {
            polar: true,
            type: 'line',
            height: 300,
        },
  			credits: {
  				enabled: false
  			},
  			title: {
  				text: data.feed.title.$t,
  				style: { fontSize: titleFontSize, fontWeight: "bold", color:titleColor},
  			},
  			colors: colorbrewer[colorPalette][colorPick].slice(),
  			xAxis: {
  				categories: XLabels
  			},
//        pane: {
//            size: '80%'
//        },

        xAxis: {
            categories: XLabels,
            tickmarkPlacement: 'on',
            lineWidth: 0
        },

        yAxis: {
            gridLineInterpolation: 'polygon',
            lineWidth: 0,
            min: 0,
            max: 10
        },

        tooltip: {
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}</b><br/>'
        },

        legend: {
            align: 'right',
            verticalAlign: 'top',
            y: 30,
            layout: 'vertical'
        },
        series: valors
    });
	});
	
	console.log('end config HighChart');
};