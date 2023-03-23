import React from 'react';

function OrderItem(props) {
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

            <td>{props.order.order_status}</td>
            <td>{props.order.order_type}</td>
            <td>{props.order.order_price}</td>
            <td>{props.order.order_quantity}</td>
            <td>{props.order.asset.symbol}/{props.order.asset_pay.symbol}</td>
        </tr>
    );
}

export default OrderItem;