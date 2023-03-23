import React, {useEffect, useState} from 'react';
import {Cookies} from "react-cookie";
import OrderItem from "./order_item";
import {json} from "react-router-dom";

function Ticker(props) {
    const cookies = new Cookies();
    const [assets,setAssets] = useState([]);
    const [subscriptionID, setSubscriptionID] = useState(null);
    const [socket, setSocket] = useState(null);
    const [buyPrice, setBuyPrice] = useState(0);
    const [sellPrice, setSellPrice] = useState(0);


    function OnAssetSelect(asset) {
        if (subscriptionID) {
            let msg = JSON.stringify({"action": "UnsubscribeMarketData", "subscriptionId": subscriptionID});
            socket.send(msg);
        }
        let msg = JSON.stringify({"action": "SubscribeMarketData", "assetId": asset});
        socket.send(msg);

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.message.messageText === 'SuccessInfo' && data.message.subscriptionId) {
                setSubscriptionID(data.message.subscriptionId)
                setSellPrice(data.message.max_price.order_price)
                setBuyPrice(data.message.min_price.order_price)
            }
            if (data.message.messageText === 'MarketDataUpdate') {
                setSellPrice(data.message.sell_price)
                setBuyPrice(data.message.buy_price)
            }
        }
    }

    useEffect(()=>{
        setSocket(new WebSocket(`ws://127.0.0.1:8000/ws/subscribe-market/`))
        fetch('http://127.0.0.1:8000/assets/getassetscross/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer `+ cookies.get('access_token'),
            }
        })
            .then(response => {
                response.json().then(data => {
                    if (data.messageType === 5 && data.message.messageText === "SuccessInfo") {
                        setAssets(data.message.responseBody)
                    }
                })
            })
    },[])
    if (assets != [])
    return (
        <div className="modal fade" id="exampleModalCenter" tabIndex="-1" role="dialog"
             aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div className="modal-dialog modal-dialog-centered" role="document">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title" id="exampleModalLongTitle">Ticker</h5>
                        <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div className="modal-body">
                        <select onChange={(event) => OnAssetSelect(event.target.value)} className="form-control text-center" id="currency-selector">
                            <option value="None">None</option>
                            {assets.map((asset, index) => {
                                return <option key={index+1} value={asset.asset_id}>{asset.asset}</option>
                            })}
                        </select><br></br>
                        <input className="form-control text-center"
                               type="number"
                               name="volume_count"
                               id="quantityInput"
                               placeholder="Amount"
                               step="any"
                               onInput={(event) => event.target.validity.valid || (event.target.value = '')}></input>
                    </div>
                    <div className="modal-footer">
                        <div className="col-6 text-center">
                            <span className="button-text" id="close-button-text">{buyPrice}$</span>
                            <input className="form-control text-center"
                                   type="number"
                                   name="volume_count"
                                   id="quantityInput"
                                   placeholder="0"
                                   step="any"
                                   onInput={(event) => event.target.validity.valid || (event.target.value = '')}></input><br></br>
                            <button type="button" className="btn btn-primary btn-block sell" data-dismiss="modal">BUY
                            </button>
                        </div>
                        <div className="col-6 text-center">
                            <span className="button-text" id="close-button-text">{sellPrice}$</span>
                            <input className="form-control text-center"
                                   type="number"
                                   name="volume_count"
                                   id="quantityInput"
                                   placeholder="0"
                                   step="any"
                                   onInput={(event) => event.target.validity.valid || (event.target.value = '')}></input><br></br>
                            <button type="button" className="btn btn-primary btn-block buy">SELL</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

}

export default Ticker;