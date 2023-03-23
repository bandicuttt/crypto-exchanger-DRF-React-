import React, {useEffect, useState} from 'react';
import {Cookies} from "react-cookie";


function Ticker(props) {

    const cookies = new Cookies();
    const [assets,setAssets] = useState([]);
    const [subscriptionID, setSubscriptionID] = useState(null);
    const [socket, setSocket] = useState(null);
    const [buyPrice, setBuyPrice] = useState(0);
    const [sellPrice, setSellPrice] = useState(0);
    const [currencyPrice, setCurrencyPrice] = useState(0);

    const handleButtonClick = () => {
        const selectedAsset = document.getElementById("currency-selector").selectedOptions[0].id;
        const amount = document.getElementById("quantityInput").value;
        const side = document.activeElement.innerText.toUpperCase();
        const sell_price = document.getElementById('sell_price').value;
        const buy_price = document.getElementById('buy_price').value;
        const selectElement = document.getElementById("currency-selector");
        const selectedOption = selectElement.options[selectElement.selectedIndex];
        const assetID = selectedOption.value;
        const assetPayID = selectedOption.id;

        function createNewOrder(order_type, order_price, amount, asset_id, asset_pay_id) {
            const url = `${process.env.REACT_APP_API_URL}/api/orders/createneworder/`;
            const body = {
                order_type: order_type,
                order_price: order_price,
                order_quantity: amount,
                asset: asset_id,
                asset_pay: asset_pay_id
            };

            fetch(url, {
                method: 'POST',
                body: JSON.stringify(body),
                headers: {
                    'Authorization': `Bearer `+ cookies.get('access_token'),
                    'Content-Type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message.messageText === 'SuccessInfo') {
                        alert('Successful')
                    } else {
                        alert('Error')
                    }

                })
                .catch(error => {
                    alert('Error')
                    console.error('Error creating order:', error);
                });
        }


        if (selectedAsset !== '') {
            if (amount > 0 && amount < 100000) {
                if (side === 'BUY') {
                    if (buy_price > 0 && buy_price < 100000) {
                        createNewOrder('buy', buy_price, amount, assetID, assetPayID);
                    } else {
                        alert('Price amount can not be less then 0 and more then 100`000')
                    }
                }
                else if (side === 'SELL') {
                    if (sell_price > 0 && sell_price < 100000) {
                        createNewOrder('sell', sell_price, amount, assetID, assetPayID);
                    } else {
                        alert('Price amount can not be less then 0 and more then 100`000')
                    }
                } else {
                    alert('Incorrect order side')
                }

            } else {
                alert('Amount can not be less then 0 and more then 100`000')
            }
        } else {
            alert('Please, select your currency')
        }

    };

    function OnAssetSelect(asset) {
        let orderPriceSell = 1;
        let orderPriceBuy = 1000;

        if (subscriptionID) {
            let msg = JSON.stringify({"action": "UnsubscribeMarketData", "subscriptionId": subscriptionID});
            socket.send(msg);
        }
        if (asset !== 'None') {
        let msg = JSON.stringify({"action": "SubscribeMarketData", "assetId": asset});
        socket.send(msg);
        }
        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.message.messageText === 'SuccessInfo' && data.message.subscriptionId) {
                setSubscriptionID(data.message.subscriptionId)
                setSellPrice(data.message.max_price.order_price)
                setBuyPrice(data.message.min_price.order_price)
                setCurrencyPrice(data.message.currency_price)
            }
            if (data.message.messageText === 'MarketDataUpdate') {
                setSellPrice(data.message.sell_price)
                setCurrencyPrice(data.message.currentPrice)
                setBuyPrice(data.message.buy_price)
            }
        }
    }

    useEffect(()=>{
        setSocket(new WebSocket(`${process.env.REACT_APP_WS_URL}/ws/subscribe-market/`))
        fetch(`${process.env.REACT_APP_API_URL}/assets/getassetscross/`, {
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
    if (assets !== [])
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
                                return <option key={index+1} value={asset.asset_pay_id} id={asset.asset_id}>{asset.asset}</option>
                            })}
                        </select><br></br>
                        <input className="form-control text-center"
                               type="number"
                               name="volume_count"
                               id="quantityInput"
                               placeholder="Amount"
                               step="0.01"
                               onInput={(event) => event.target.validity.valid || (event.target.value = '')}></input>
                    </div>
                    <span className="text-center">Asset price: {currencyPrice}$</span>
                    <div className="modal-footer">
                        <div className="col-6 text-center">
                            <span className="button-text" id="close-button-text">{buyPrice}$</span>
                            <input className="form-control text-center"
                                   type="number"
                                   name="volume_count"
                                   id="buy_price"
                                   placeholder="0"
                                   step="0.01"
                                   onInput={(event) => event.target.validity.valid || (event.target.value = '')}></input><br></br>
                            <button
                                type="button"
                                className="btn btn-primary btn-block sell"
                                // data-dismiss="modal"
                                onClick={handleButtonClick}
                            >
                                BUY
                            </button>
                        </div>

                        <div className="col-6 text-center">
                            <span className="button-text" id="close-button-text">{sellPrice}$</span>
                            <input className="form-control text-center"
                                   type="number"
                                   name="volume_count"
                                   id="sell_price"
                                   placeholder="0"
                                   step="any"
                                   onInput={(event) => event.target.validity.valid || (event.target.value = '')}></input><br></br>
                            <button
                                type="button"
                                className="btn btn-primary btn-block buy"
                                onClick={handleButtonClick}
                                // data-dismiss="modal"
                            >
                                SELL
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

}

export default Ticker;