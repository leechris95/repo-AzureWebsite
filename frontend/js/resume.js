window.addEventListener('DOMContentLoaded', (event) => {
    getVisitCount();
})

const functionApi = "https://myazure-app1315x.azurewebsites.net/api/update-entity?Row_key=staticwebsite1315x_res";
//const functionApi = "http://localhost:7071/api/update-entity";

const getVisitCount = () => {
    let count = 0;
    fetch(functionApi).then(response => {
        return response.json()
    }).then(response => {
        console.log('Website called function API.');
        count = response.VisitorCount;
        document.getElementById('webpage-counter').innerText = count;
    }).catch(function(error){
        console.log(error);
    });
    return count;
}