	var StretchDialog = function(input, output, onOK){

	Dialog.apply(this, arguments);

	this._input = input;
	this._output = output;
	this.setInput(input);
	this.setOutput(output);

	this.initFolderEvent();

	this._onOK = onOK;
}

extend(StretchDialog, Dialog)


StretchDialog.prototype.initFolderEvent = function(){

	var dlg = this;
	this._win.find(".dialog_folder").each(function(){
		$(this).click(function(){
			$(this).prev().find('.dialog_input').each(function(){
				//设置输入影像数据路径的值
				var file_dlg = new FileDialog(dlg._input,"choose", function(){
					dlg.setInput(this.getFilePath());
				});
				file_dlg.show();
			})

			$(this).prev().find('.dialog_output').each(function(){
				//设置输入影像数据路径的值
				var file_dlg = new FileDialog(dlg._output,"new", function(){
					dlg.setOutput(this.getFilePath());
				});
				file_dlg.show();
			})
		});
	})
}

StretchDialog.prototype.initCloseEvent = function(){
	var dlg = this;
	this._win.find(".dialog_exit:first").click(function(){
		dlg.destory();
	});

	this._win.find("#dlg_btn_exit:first").click(function(){
		dlg.destory();
	});
}

StretchDialog.prototype.initOkEvent = function(){
	var dlg = this;

	this._win.find("#dlg_btn_ok:first").click(function(){
		dlg._input  = dlg._win.find(".dialog_input:first").val();
		dlg._output = dlg._win.find(".dialog_output:first").val();
		dlg.destory();

		if(dlg._onOK){
			dlg._onOK();
		}
	});
}


StretchDialog.prototype.getInput = function(){
	return this._input;
}

StretchDialog.prototype.getOutput = function(){
	return this._output;
}

StretchDialog.prototype.setInput = function(input){
	this._input = input ? input : "/";
	this._win.find('.dialog_input').attr("value", input);
}

StretchDialog.prototype.setOutput = function(output){
	this._output = output ? output : "/";
	this._win.find('.dialog_output').attr("value", output);
}

StretchDialog.prototype.create = function(){
	var html =   "<div class='func_dialog dialog'>"
			+"<div class='titlebar'>"
			+"	<div class='dialog_title'>拉伸</div>"
			+"	<div class='dialog_exit'></div>"
			+"</div>"
			+"<div class='dialog_main'>"
			+"	<div class='dialog_item'>"
			+"		<div>"
			+"			<div class='dialog_item_icon'></div>"
			+"			<div class='dialog_item_title'>输入影像:</div>"
			+"		</div>"
			+"		<div>"
			+"			<div style='float:left;'><input type='text' class='dialog_input'></div>"
			+"			<div class='dialog_folder'></div>"
			+"		</div>"
			+"	</div>"
			+"	<div class='dialog_item'>"
			+"		<div>"
			+"			<div class='dialog_item_icon'></div>"
			+"			<div class='dialog_item_title'>输出影像:</div>"
			+"		</div>"
			+"		<div>"
			+"			<div style='float:left;'><input type='text' class='dialog_output'></div>"
			+"			<div class='dialog_folder'></div>"
			+"		</div>"
			+"	</div>"
			+"</div>"
			+"<div class='dialog_bottom'>"
			+"	<ul>"
			+"		<li>"
			+"			<a href='javascript:void(0)' id='dlg_btn_ok'>确定</a>"
			+"		</li>"
			+"		<li>"
			+"			<a href='javascript:void(0)' id='dlg_btn_exit'>取消</a>"
			+"		</li>"
			+"	</ul>"
			+"</div>";
	$(".func_dialog").remove();
	var dlg = $(html);
	$('body').append(dlg);
	return dlg;
}
