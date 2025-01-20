document.querySelectorAll('.tom-tag').forEach((el)=>{
	// let settings = {};
 	// new TomSelect(el,settings);
	 new TomSelect(el,{
		 // #tom-tags
		 persist: false,
		 createOnBlur: true,
		 create: true,
		//  render:{
		// 	 option: function(data) {
	 
		// 		 const div = document.createElement('div');
		// 		 div.className = 'd-flex align-items-center';
	 
		// 		 const span = document.createElement('span');
		// 		 span.className = 'flex-grow-1';
		// 		 span.innerText = data.text;
		// 		 div.append(span);
	 
		// 		 const a = document.createElement('a');
		// 		 a.innerText = '#';
		// 		 a.className = 'btn btn-sm btn-light';
		// 		 div.append(a);
		// 		 a.addEventListener('click',function(evt){
		// 			 evt.stopPropagation();
		// 			 alert(`You clicked # within the "${data.text}" option`);
		// 		 });
	 
		// 		 return div;
		// 	 },
		//  }
	 });
});