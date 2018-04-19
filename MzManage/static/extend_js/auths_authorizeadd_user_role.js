$(function(){

//--比较两个表，冻结已添加的表
	function lockHoststr(){ //创建一个数组，获取添加的hostid，out表中的host_id与之做比较
		var hostIdList= new Array()
		$("#add_auth_table tr").each(function(){
			var host_id=$(this).attr("host_id")
			hostIdList.push(host_id)
		})
		$("#outhosts tr").each(function(){
			var out_id=$(this).attr("host_id")
			if ( $.inArray(out_id,hostIdList) != -1 ){
				$(this).addClass("tr-disabled ").children().first().children().removeClass("checked").iCheck('disable')
			}
		})
	};

	$('#add_table input[type="checkbox"]').iCheck("uncheck")
	//Enable iCheck plugin for checkboxes
	//iCheck for checkbox and radio inputs
	$('#add_table input[type="checkbox"]').iCheck({
			checkboxClass: 'icheckbox_flat-blue'
		});
	//Enable check and uncheck all functionality
	$("#add_table th .checkbox-toggle").click(function () {
			var clicks = $(this).data('clicks');
			if (clicks) {
				$("#add_table div[aria-disabled!='true'] input[type='checkbox']").iCheck("uncheck");
				$(".fa", this).removeClass("fa-check-square-o").addClass('fa-square-o');
			}else{
				$("#add_table input[type='checkbox']").iCheck("check");
				$(".fa", this).removeClass("fa-square-o").addClass('fa-check-square-o');
			}
			 $(this).data("clicks", !clicks);		
	});

	//Enable check and uncheck all functionality
	$("#auth_table th .checkbox-toggle").click(function () {
			var clicks = $(this).data('clicks');
			if (clicks) {
				$("#add_auth_table input[type='checkbox']").iCheck("uncheck");
				$(".fa", this).removeClass("fa-check-square-o").addClass('fa-square-o');
			}else{
				$("#add_auth_table input[type='checkbox']").iCheck("check");
				$(".fa", this).removeClass("fa-square-o").addClass('fa-check-square-o');
			}
			 $(this).data("clicks", !clicks);		
	});

	//-- 分页获取主机
	$("a[ajax_href]").click(function(){
		$("#add_table th .checkbox-toggle").children().removeClass("fa-check-square-o").addClass("fa-square-o")
		$("#auth_table th .checkbox-toggle").children().removeClass("fa-check-square-o").addClass("fa-square-o")
		if ( $(this).attr("ajax_href") != "null" ){
			var page_url = $(this).attr("ajax_href")
			if ($(this).attr("a_tag")=="true"){
				$(this).parent().siblings().removeClass("active")
				$(this).parent().addClass("active")
			}
			var mythis = $(this)
			$.ajax({
				type:"GET",
				url:page_url,
				dataType:"json",
				success:function(data){
					$("#outhosts").html("")
					var tmp_html=""
					for (host in data.hosts){
						var tmp_html = "<tr host_id="+data.hosts[host]["id"]+"><td><input type='checkbox' /></td><td>"+data.hosts[host]["hostName"]+"</td><td>"+data.hosts[host]["hostIP"]+"</td><td>"+data.hosts[host]["hostGroup"]+"</td></tr>"	
						$("#outhosts").append(tmp_html)
					}
					//锁定已经选中主机
					lockHoststr()
					$('.hostbox-messages input[type="checkbox"]').iCheck({
					    checkboxClass: 'icheckbox_flat-blue',
							radioClass: 'iradio_flat-blue'
					  });
					//上一页下一页样式
					//上一页样式
					if (data.prev != null){
						$("#outhosts_previous").removeClass("disabled")
					}else{
						$("#outhosts_previous").addClass("disabled").children().attr("ajax_href","null")
					}
					var prev_url=$("#outhosts_paginate ul .active").prev().children().attr("ajax_href")
					var next_url=$("#outhosts_paginate ul .active").next().children().attr("ajax_href")
					$("#outhosts_previous").children().attr("ajax_href",prev_url)
					$("#outhosts_next").children().attr("ajax_href",next_url)
					if (mythis.parent().attr("id") == "outhosts_previous"){
						if ($("#outhosts_paginate ul .active").prev().attr("id") == "outhosts_previous"){
							$("#outhosts_paginate ul .active").prev().addClass("disabled").children().attr("ajax_href","null")
						}else{
							$("#outhosts_paginate ul .active").removeClass("active").prev().addClass("active")
							var prev_url=$("#outhosts_paginate ul .active").prev().children().attr("ajax_href")
							var next_url=$("#outhosts_paginate ul .active").next().children().attr("ajax_href")
							$("#outhosts_previous").children().attr("ajax_href",prev_url)
							$("#outhosts_next").children().attr("ajax_href",next_url)
						}
					}
					//--下一页样式
					if (data.next != null){
						$("#outhosts_next").removeClass("disabled")
					}else{
						$("#outhosts_next").addClass("disabled").children().attr("ajax_href","null")
					}
					var next_url=$("#outhosts_paginate ul .active").next().children().attr("ajax_href")
					var prev_url=$("#outhosts_paginate ul .active").prev().children().attr("ajax_href")
					$("#outhosts_next").children().attr("ajax_href",next_url)
					$("#outhosts_previous").children().attr("ajax_href",prev_url)
					if (mythis.parent().attr("id") == "outhosts_next"){
						if ($("#outhosts_paginate ul .active").next().attr("id") == "outhosts_next"){
							$("#outhosts_paginate ul .active").next().addClass("disabled").children().attr("ajax_href","null")
						}else{
							$("#outhosts_paginate ul .active").removeClass("active").next().addClass("active")
							var next_url=$("#outhosts_paginate ul .active").next().children().attr("ajax_href")
							var prev_url=$("#outhosts_paginate ul .active").prev().children().attr("ajax_href")
							$("#outhosts_previous").children().attr("ajax_href",prev_url)
							$("#outhosts_next").children().attr("ajax_href",next_url)
						}
					}
				}
			})
		}
	});
//-------end
	//--添加主机按钮
	$("#addHostBtn").click(function(){
		if ($("#outhosts td .checked").length == 0){
			$('#addModal').modal('toggle')
		}else{
			//添加界面	
			$("#model_hosts").html("")
			$("#outhosts td .checked").each(function(){
				var host_id = $(this).parent().parent().attr("host_id")
				var check_tr = $(this).parent().parent().html()
				$("#model_hosts").append("<tr host_id="+host_id+">"+check_tr+"</tr>")
			})
		}
	});	
	//--end 添加主机
//---添加确认授权表
	$("#model_auth").click(function(){
		var selected_role = $("#select_role").val()
		$("#model_hosts tr").each(function(){
			var host_id = $(this).attr("host_id")
			var tmp_html=$(this).children().last().text(selected_role).parent().html()	
			$("#add_auth_table").append("<tr host_id="+host_id+">"+tmp_html+"</tr>")
		})
			$("#add_auth_table td div").parent().html("").append("<input  type='checkbox' />")
			$('#add_auth_table input[type="checkbox"]').iCheck({
				    checkboxClass: 'icheckbox_flat-blue' //确认授权表中checkbox样式
				});
			$('#addModal').modal('toggle')
			//$("#outhosts td .checked").removeClass("checked").iCheck('disable').parent().parent().parent().addClass("tr-disabled ")
			lockHoststr()

	})
//---end 模态里的授权
//-- 确认授权按钮
	$("#confirmAuth").click(function(){
		if ($("#add_auth_table tr .checked").length != 0){
			var user_id = $("#user_tag").attr("user_id")
			var hostRole = {}
			$("#add_auth_table tr .checked").each(function(){
				var host_id = $(this).parent().parent().attr("host_id")
				var role = $(this).parent().siblings().last().text()
				hostRole[host_id]=role
			})
			//post数据给用户授权
			$.ajax({
				url:"/auths/authorizeuser/ajax/authhostsuser/",
				type:"POST",
				data:{"data":JSON.stringify({"host_role":hostRole,"user_id":user_id})},
				dataType:"json",
				success:function(data){
					var domain = window.location.host;
					window.location.href="http://"+domain+"/auths/authorizeuser/userpage-"+user_id
				},
				error:function(data){
					var domain = window.location.host;
					window.location.href="http://"+domain+"/auths/authorizeuser/userpage-"+user_id	
				}
			})
		}
	});
	
//-- end确认授权更改数据库
//-----	
});

