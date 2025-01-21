function getColor(){ 
    return "hsl(" + 360 * Math.random() + ',' +
               (25 + 70 * Math.random()) + '%,' + 
               (85 + 10 * Math.random()) + '%)'
  }
  
  
const rand_els = document.getElementsByClassName("rand-colored");
// console.log(rand_els)
// Generate 20 colors
rand_els.forEach((el) => {
    console.log(el);
    el.style.backgroundColor = `${getColor()};`
    // document.body.appendChild(item);
  });