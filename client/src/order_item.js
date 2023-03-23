import React from 'react';

function OrderItem(props) {
    function updateOrderStatus(orderId) {
        const url = `${process.env.REACT_APP_API_URL}/api/orders/updateorder/${orderId}/`;
        const body = { order_status: 'cancelled' };

        fetch(url, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        })
            .then(response => response.json())
            .then(data => {
                if (data.message.messageText === 'SuccessInfo'){
                    alert(`Your order ${orderId} has been updated to cancelled`)
                }
            })
            .catch(error => console.error(error));
    }
    return (
        <tr scope="row">
            <th scope="row">
                <label className="control control--checkbox">
                    <input type="checkbox"></input>
                    <div className="control__indicator"></div>
                </label>
            </th>

            <td>
                {props.order.id}
            </td>

            <td>
                {props.order.created_at}
            </td>

            <td>
                {props.order.updated_at}
            </td>

            <td>
                {props.order.order_status === 'active' ? (
                    // eslint-disable-next-line react/style-prop-object
                    <a onClick={() => updateOrderStatus(props.order.id)} className='btn btn-primary cancel-order' style={{ color: 'white' }}>Cancel</a>

                ) : (
                    props.order.order_status
                )}

            </td>
            <td>{props.order.order_type}</td>
            <td>{props.order.order_price}</td>
            <td>{props.order.order_quantity}</td>
            <td>{props.order.asset_pay.symbol}/{props.order.asset.symbol}</td>
        </tr>
    );
}

export default OrderItem;