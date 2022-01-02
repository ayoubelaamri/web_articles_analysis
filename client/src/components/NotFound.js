import React from 'react'

export default function NotFound() {
    return (
        <div class="container text-center mt-5">
            <div class="row">
                <div class="col-md-12">
                    <div class="error-template">
                        <h1>Oops!</h1>
                        <h2>Page Not Found</h2>
                        <div class="error-details">
                            Sorry, an error has occured, Requested page not found!
                        </div>
                        <div class="error-actions">
                            <a href="/" class="btn btn-primary btn-lg mt-3"><span class="fa fa-home mr-2"></span>Take Me Home </a>
                            <a href="#" class="btn btn-default btn-lg mt-3"><span class="fa fa-envelope mr-2"></span> Contact Support </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
