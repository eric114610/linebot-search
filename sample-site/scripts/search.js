// Update this variable to point to your domain.
var apigatewayendpoint = 'https://o0p2k383h8.execute-api.ap-northeast-3.amazonaws.com/opensearch-api-test/';
var loadingdiv = $('#loading');
var noresults = $('#noresults');
var resultdiv = $('#results');
var searchbox = $('input#search');
var searchbox2 = $('input#search2');
var searchbox3 = $('input#search3');
var searchbox4 = $('input#search4');
var timer = 0;

// Executes the search function 250 milliseconds after user stops typing
// searchbox.keyup(function () {
//   clearTimeout(timer);
//   timer = setTimeout(search, 250);
// });

// async function search() {
//   // Clear results before searching
//   noresults.hide();
//   resultdiv.empty();
//   loadingdiv.show();
//   // Get the query from the user
//   let query = searchbox.val();
//   // Only run a query if the string contains at least three characters
//   if (query.length > 2) {
//     // Make the HTTP request with the query as a parameter and wait for the JSON results
//     let response = await $.get(apigatewayendpoint, { q: query, size: 25 }, 'json');
//     // Get the part of the JSON response that we care about
//     console.log(response['hits']['hits'])
//     let results = response['hits']['hits'];
//     if (results.length > 0) {
//       loadingdiv.hide();
//       // Iterate through the results and write them to HTML
//       resultdiv.append('<p>Found ' + results.length + ' results.</p>');
//       for (var item in results) {
//         let url = 'https://www.imdb.com/title/' + results[item]._id;
//         let image = results[item]._source.image_url;
//         let title = results[item]._source.title;
//         let plot = results[item]._source.plot;
//         let year = results[item]._source.year;
//         // Construct the full HTML string that we want to append to the div
//         resultdiv.append('<div class="result">' +
//         '<a href="' + url + '"><img src="' + image + '" onerror="imageError(this)"></a>' +
//         '<div><h2><a href="' + url + '">' + title + '</a></h2><p>' + year + ' &mdash; ' + plot + '</p></div></div>');
//       }
//     } else {
//       noresults.show();
//     }
//   } else {
//     await $.get(apigatewayendpoint, { q: query, size: 25 }, 'json');
//   }
//   loadingdiv.hide();
// }

// Tiny function to catch images that fail to load and replace them
function imageError(image) {
  image.src = 'images/no-image.png';
}

async function myGet() {
    let index = searchbox.val();
    let _message = searchbox2.val();
    let _embedding = searchbox3.val();
    let _id = searchbox4.val();
    let response = await $.get(apigatewayendpoint, { type: "Get", size: 25 , q: index, message: _message, embedding: _embedding, id: _id}, 'json');
    // Get the part of the JSON response that we care about
    console.log(response)
}

async function myPost() {
  let index = searchbox.val();
    let _message = searchbox2.val();
    let _embedding = searchbox3.val();
    let _id = searchbox4.val();
    let response = await $.get(apigatewayendpoint, { type: "Post", size: 25 , q: index, message: _message, embedding: _embedding, id: _id}, 'json');
  // Get the part of the JSON response that we care about
  console.log(response)
}

async function myPut() {
  let index = searchbox.val();
    let _message = searchbox2.val();
    let _embedding = searchbox3.val();
    let _id = searchbox4.val();
    let response = await $.get(apigatewayendpoint, { type: "Put", size: 25 , q: index, message: _message, embedding: _embedding, id: _id}, 'json');
  // Get the part of the JSON response that we care about
  console.log(response)
}