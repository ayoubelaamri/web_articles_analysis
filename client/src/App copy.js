import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  // const [data, setData] = useState(null);
  const [date, setDate] = useState("2017");
  const [site, setSite] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  
  function setKeyword(e) {
    setSearchTerm(e.target.value);
  }
  function setSource(e) {
    setSite(e.target.value);
  }
  function setYear(e) {
    setDate(e.target.value);
    console.log(date);
  }

  function scrape(e) {
    e.preventDefault();
    fetch('/run/'+site+'/'+date+'/'+searchTerm)
      // .then(res => res.json()).then(data => {
      //   setData(data);
      // });
    // console.log(data);
  }

  return (
    <div className="App">

      <div class="container">
        <div class="row height d-flex justify-content-center align-items-center">
            <div class="col-md-6 text-center">
              <form onSubmit={scrape}>
              
                <div class="col-12">
                  <input class="checkbox-tools" type="radio" name="site" id="tool-1" autocomplete="off" value="all" onChange={setSource} checked={site==="all"} />
                  <label class="for-checkbox-tools" for="tool-1">
                    {/* <i class='uil uil-line-alt'></i> */}
                    All
                  </label><input class="checkbox-tools" type="radio" name="site" id="tool-2" autocomplete="off" value="pubmed" onChange={setSource} checked={site==="pubmed"} />
                  <label class="for-checkbox-tools" for="tool-2">
                    {/* <i class='uil uil-vector-square'></i> */}
                    PubMed
                  </label><input class="checkbox-tools" type="radio" name="site" id="tool-3" autocomplete="off" value="ieee" onChange={setSource} checked={site==="ieee"} />
                  <label class="for-checkbox-tools" for="tool-3">
                    {/* <i class='uil uil-ruler'></i> */}
                    ieee
                  </label><input class="checkbox-tools" type="radio" name="site" id="tool-4" autocomplete="off" value="scopus" onChange={setSource} checked={site==="scopus"} />
                  <label class="for-checkbox-tools" for="tool-4">
                    {/* <i class='uil uil-crop-alt'></i> */}
                    Scopus
                  </label>
                </div>

                <select onChange={setYear}>
                  <option value="2021" selected={date==="2021"}>2021</option>
                  <option value="2020" selected={date==="2020"}>2020</option>
                  <option value="2019" selected={date==="2019"}>2019</option>
                  <option value="2018" selected={date==="2018"}>2018</option>
                  <option value="2017" selected={date==="2017"}>2017</option>
                  <option value="2016" selected={date==="2016"}>2016</option>
                  <option value="2015" selected={date==="2015"}>2015</option>
                </select>

                <div class="form mt-3"> <i class="fa fa-search"></i> <input value={searchTerm} onChange={setKeyword} type="text" class="form-control form-input" placeholder="Scrape anything..."/> <span class="left-pan"><i class="fa fa-microphone"></i></span> </div>

              </form>
            </div>
        </div>
      </div>

      

    </div>
  );
}

export default App;
