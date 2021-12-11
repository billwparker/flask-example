d3.json("api/movies").then((data) => {

  console.log(data)

  // $(document).ready(function() {
  $('#example').DataTable( {
      data: data['table'],
      columns: [
          { title: "Title" },
          { title: "Director" },
          { title: "Year" },
          { title: "Rating" },
          { title: "Votes" },
          { title: "Score" },
      ]
  } );

})

function buildYearChart(year) {

  console.log(year);

  d3.json(`api/years/${year}`).then((data) => {

    var trace1 = {
      type: 'bar',
      x: data['rating'],
      y: data['votes'],
      marker: {
          color: '#C8A2C8',
      }
    };
    
    var data = [ trace1 ];
    
    var layout = { 
      title: 'Years',
    };
    
    var config = {responsive: true}
    
    Plotly.newPlot('bar', data, layout, config );
  
  })
}

function buildDirectorChart(director) {

  console.log(director);

  d3.json(`api/directors/${director}`).then((data) => {

    console.log(data)
  
    var trace1 = {
      type: 'bar',
      x: data['labels'],
      y: data['scores'],
      marker: {
          color: '#C8A2C8',
      }
    };
    
    var data = [ trace1 ];
    
    var layout = { 
      title: 'Directors',
    };
    
    var config = {responsive: true}
    
    Plotly.newPlot('v-bar', data, layout, config );
  
  })
}


function optionYearChanged(newYear) {
  buildYearChart(newYear);
}

function optionDirectorChanged(newDirector) {
  buildDirectorChart(newDirector);
}

buildYearChart("before")

buildDirectorChart("chaplin")


