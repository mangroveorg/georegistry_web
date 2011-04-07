(function($){
    var table;
    var wrapDiv;
    function BuildGrMapTable(data) {
        wrapDiv = $("<div />");
        var bcs = [$("<div />", {'class':'breadcrumbs high'}), $("<div />", {'class':'breadcrumbs low'})]
        var innerMain = $("<div />", {'id':'inner-main'});
        innerMain.append($("<div />", {'id': 'georeg-content'}))
                    .append($("<div />", {'id': 'map-content'}));
        
        wrapDiv.append(bcs[0])
                .append(innerMain)
                .append(bcs[1]);
        
        var Features = false;
		$(function(){
            startMap()
            
			if(data && data.features && data.features instanceof Array) {
				Features = [];
				$.each(data.features, function(){
				    var ll = this.geometry.coordinates;
				    var opts = {
				        position: new google.maps.LatLng(ll[0], ll[1])
				    }
				    opts.marker = new google.maps.Marker({
				        'title': 'Title',
				        position: opts.position
				    });
				    google.maps.event.addListener(opts.marker, 'click', function(){
				        alert("DoSomething");
	        		});
					Features.push($.extend(this, opts));
				});

				var tr,
				    table = $("<table />", {id: 'georeg-items'})
								.css({'width':'100%'});

				$(Features).each(function(){
					tr = $("<tr />");
					tr.append($("<td />")
						.html($("<a />", {href: this.properties.href})
						.text(this.properties.name)));
                    
					tr.data('geo-data', this);
					tr.data('marker', this.marker);

					var districtTd = $("<td />")
						.text(this.properties.level3_admin_boarder_code);
					tr.append(districtTd)
					table.append(tr);
				});

				$('#georeg-content', wrapDiv).html(table);
			}
			var mapContent = $('#map-content', wrapDiv)
				.css({'position':'absolute','top':'0',left:'100%', 'background-color':'#f00',
							'width':'50%', 'height': '100%'}).text(' ');

			$('#inner-main', wrapDiv).css({'position':'relative', 'overflow':'hidden'});

			var weHaveAMapAlready = false;
			function startMap(opts) {
				if(!weHaveAMapAlready) {
					if(typeof(google)!=='undefined') {
						//create the map object
						var options = {
							zoom: 11,
							mapTypeId: 'satellite',
							center: new google.maps.LatLng(9.243092645104804, 7.9156494140625)
						}
                        
						map = new google.maps.Map($("#map-content", wrapDiv).get(0), options)
					}
					weHaveAMapAlready = true;
				}
			}
			var pointsLoaded = false;
			function ensurePointsLoaded() {
			    if(!pointsLoaded) {
			        $(Features).each(function(){
			            this.marker.setMap(map);
			        })
			    }
			}

			var marker = false;
			function splitScreen(opts){
				startMap(opts);
					//create a "marker" for the destination
//					var pointPosition = new google.maps.LatLng(ll[0], ll[1]);
                    // marker = new google.maps.Marker({
                    //  title: 'Title',
                    //  position: pointPosition
                    // });
                    // 
                    // //set the marker's map to our map
                    // marker.setMap(map);
                    // 
                    // map.panTo(pointPosition);
//					map.setZoom(8);
				$('#georeg-content', wrapDiv).animate({'overflow':'hidden', 'width':'50%'});
				$("#map-content", wrapDiv).animate({'left':'50%'});
				ensurePointsLoaded();
			}
			function fullScreenMap(){
				startMap()
				$('#georeg-content', wrapDiv).animate({'left':'100%'});
				$('#map-content', wrapDiv).animate({'left':0, 'width':'100%'});
				ensurePointsLoaded();
			}
			function fullScreenList() {
				$('#georeg-content', wrapDiv).animate({'width':'100%', 'left':0});
				$("#map-content", wrapDiv).animate({'left':'100%'});
				ensurePointsLoaded();
			}

			$('table#georeg-items', wrapDiv).delegate('a', 'click', function(evt){
			    ensurePointsLoaded();
				var geoData = $(this).parents('tr').data('geo-data');
				var marker = $(this).parents('tr').data('marker');

                map.panTo(marker.position);
                marker.setMap(map);

				if(geoData && geoData.geometry && geoData.geometry.coordinates) {
					var latLng = geoData.geometry.coordinates;
					splitScreen({
						destinationLatLng: latLng
					});
				}

				evt.preventDefault();
			});

			(function(){
			    var breadcrumbs = $("div.breadcrumbs", wrapDiv)
			            .css({'padding':'6px 0', 'text-align':'center'})
				
			    var bcL = $("<a />", {href:'#', 'class':'slide-link'}).css({'color':'black','border':'1px solid #444','text-decoration':'none', 'padding':'2px 6px', 'margin':'1px 5px 1px 0'});
			    
			    var listLink = bcL.clone().addClass('full-list')
			            .text('Full List')
			            .appendTo(breadcrumbs);
			    
				var slideLink = bcL.clone().addClass('split-screen')
				        .text('Split the Screen')
			            .appendTo(breadcrumbs);
				        
				var mapLink = bcL.clone().addClass('full-map')
				        .text('Full Map View')
			            .appendTo(breadcrumbs);
	
				breadcrumbs.find('a.slide-link.full-map').click(function(){
					fullScreenMap();
				});

				breadcrumbs.find('a.slide-link.split-screen').click(function(){
					splitScreen();
				});

				breadcrumbs.find('a.slide-link.full-list').click(function(){
					fullScreenList();
				});
			})();
		});
        return wrapDiv;
    }
    
    $.buildGrMapTable = BuildGrMapTable;
})(jQuery)