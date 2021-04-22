window.onload = function () {
    var autoCompletejs = new autoComplete({
        data: {
            src: async function () {
                // First, load placeholder text..
                document.querySelector("#autoComplete").setAttribute("placeholder", "Loading...");

                // Then, fetch and return external data:
                var source = await fetch("/patients");
                var data = await source.json();

                return data;
            },
            key: ["id","firstName","lastName"]
        },
        placeHolder: "Patient...",
        selector: "#autoComplete",
        threshold: 0,
        searchEngine: "strict",
        highlight: true,
        maxResults: 10,
        resultsList: {
            container: function(source) {
                resultsListID = "autoComplete_results_list";
                return resultsListID;
            },
            destination: document.querySelector("#autoComplete"),
            position: "afterend"
        },
        resultItem: function(data, source) {
            return `${data.match}`;
        },
        onSelection: function(feedback) {
            console.log("feedback: "+feedback)
            var selection = feedback.selection.value;
            document.querySelector(".selection").innerHTML = 
             '<a href="patient/'+selection.id+'/VaccTrackApp">'+selection.firstName+' '+selection.lastName+ ' (id: ' + selection.id + ')</a>';
            document.querySelector("#autoComplete").value = "";
            //document.querySelector("#autoComplete").setAttribute("placeholder", selection.name);
        }
    });
};
