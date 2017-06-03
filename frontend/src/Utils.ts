/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

namespace ChannelsDB {
    "use strict";

    function readData(data: XMLHttpRequest): Promise<any> {
        return new Promise<any>((resolve, reject) => {           
            data.onerror = e => {
                let error = (<FileReader>e.target).error;
                reject(error ? error : 'Failed.');
            };   
            data.onload = e => resolve(e);
        });
    }

    class RequestPool {
        private static pool: XMLHttpRequest[] = [];
        private static poolSize = 15;

        static get() {
            if (this.pool.length) return this.pool.pop()!;
            return new XMLHttpRequest();
        }

        static emptyFunc() { } 

        static deposit(req: XMLHttpRequest) {
            if (this.pool.length < this.poolSize) {
                req.onabort = RequestPool.emptyFunc;
                req.onerror = RequestPool.emptyFunc;
                req.onload = RequestPool.emptyFunc;
                req.onprogress = RequestPool.emptyFunc;
                this.pool.push();
            }
        }
    }
    
    function processAjax(e: any) {
        const req = (e.target as XMLHttpRequest);
        if (req.status >= 200 && req.status < 400) {
            const text = JSON.parse(e.target.responseText);
            RequestPool.deposit(e.target);
            return text;
        } else {
            const status = req.statusText;        
            RequestPool.deposit(e.target);
            throw status;            
        }
    }
    
    export async function ajaxGetJson<T>(url: string): Promise<T>  {
        const xhttp = RequestPool.get();                    
        xhttp.open('get', url, true);
        xhttp.responseType = "text";
        xhttp.send();        
        const e = await readData(xhttp);
        return processAjax(e);
    } 
}