$(function(){
	$(" a[ajax_href!="#"]").click(function(){
		var host_url = $(this).attr["ajax_href"]
		console.log(host_url)
	
	})



});
