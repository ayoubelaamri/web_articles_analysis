import React, {useState} from 'react';
import { Switch, Route, Redirect } from "react-router-dom";
import Dash from './Dash';

export default function Landing() {
    const [date, setDate] = useState("2017");
    const [site, setSite] = useState("all");
    const [searchTerm, setSearchTerm] = useState("");

    const [data, setData] = useState(null);
    const [status, setStatus] = useState(null);
    
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
    
    const scrape = async(e) => {
        setStatus(1);
        e.preventDefault();
        await fetch('/run/'+site+'/'+date+'/'+searchTerm)
        .then(res => {return res.json()}).then(data => {
            if(data.redirect === true) {
                window.location.replace("http://localhost:3000/dashboard");
                setStatus(null); 
            }
            else {
                setStatus(-1); 
                console.log("Can't redirect ! ERROR with api response .."); 
            }   
        });  
    }

    return (
        <div>
            <div id="booking" class="section">
                <div class="section-center">
                    <div class="container">
                        <form onSubmit={scrape}>
                            <div class="row justify-content-center">
                                {
                                    !status ? (
                                        <>
                                        <div class="col-md-7 col-md-push-5">
                                            <div class="booking-cta">
                                                <h1>Scrape Web Articles</h1>
                                                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Animi facere, soluta magnam consectetur molestias itaque.
                                                </p>
                                                <div class="row form">
                                                    <div class="col-8"><input class="form-control search-input" value={searchTerm} onChange={setKeyword} type="text" placeholder="Scrape anything here .."/></div>
                                                    <div class="col-4"><button class="submit-btn" type="submit"><i className="fa fa-search" /></button></div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-4 col-md-pull-6">
                                            <div class="booking-form">
                                                <h1 class="text-center">Advanced Search</h1>
                                                <div class="form-group">
                                                    <span class="form-label">Sources :</span>
                                                    <select onChange={setSource} class="form-control">
                                                        <option value="all" selected={site==="all"}>All disponible sources</option>
                                                        <option value="scopus" selected={site==="scopus"}>Scopus (https://www.scopus.com)</option>
                                                        <option value="pubmed" selected={site==="pubmed"}>Pubmed (https://www.pubmed.gov)</option>
                                                        <option value="ieee" selected={site==="ieee"}>IEEE (https://www.ieee.com)</option>
                                                    </select>
                                                    <span class="select-arrow"></span>
                                                </div>
                                                <div class="row">
                                                    <div class="col-sm-6">
                                                        <div class="form-group">
                                                            <span class="form-label">From :</span>
                                                            <input onChange={setYear} class="form-control" type="date" />
                                                        </div>
                                                    </div>
                                                    <div class="col-sm-6">
                                                        <div class="form-group">
                                                            <span class="form-label">To :</span>
                                                            <input class="form-control" type="date" />
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        </>
                                    ):(
                                        status === 1 ? (
                                            <>
                                                <div className='col-6 text-center'>
                                                        <div style={{scale:'3'}} class="spinner-border text-light" role="status">
                                                            <span class="sr-only">Loading...</span>
                                                        </div>
                                                        <div className='mt-5' style={{color:'#fff'}}>Please wait, we are collecting data for you ...</div>
                                                </div>
                                            </>
                                        ):(
                                            <>
                                                <div className='col-6 text-center'>
                                                        <div style={{scale:'5', color:'#fff'}} class="fa fa-exclamation-triangle" role="status"></div>
                                                        <i className='fa fa-exclamation-triangle'></i>
                                                        <div className='mt-5' style={{color:'#fff'}}>ERROR: Something went wrong !</div>
                                                        <div className='' style={{color:'#fff'}}>Please Retry Again !</div>
                                                </div>
                                            </>
                                        )
                                    )
                                }
                            </div>
                        </form>
                    </div>

                    {/* <footer>
                        By: AYOUB ELAAMRI.
                    </footer> */}

                </div>
            </div>
        </div>
    )
}
