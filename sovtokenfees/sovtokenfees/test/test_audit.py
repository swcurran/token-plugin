from sovtoken.constants import ADDRESS, AMOUNT, SEQNO

from plenum.common.constants import TXN_PAYLOAD, TXN_PAYLOAD_DATA, AUDIT_TXN_LEDGERS_SIZE, AUDIT_TXN_LEDGER_ROOT
from plenum.common.txn_util import get_seq_no


def test_revert_fees_reset(looper, helpers, txnPoolNodeSet,
                           nodeSetWithIntegratedTokenPlugin,
                           fees,
                           xfer_mint_tokens, xfer_addresses,
                           sdk_pool_handle):
    nodes = nodeSetWithIntegratedTokenPlugin

    # nodes[0].
    [address_giver, address_receiver] = xfer_addresses
    seq_no = get_seq_no(xfer_mint_tokens)
    inputs = [{ADDRESS: address_giver, SEQNO: seq_no}]
    outputs = [{ADDRESS: address_receiver, AMOUNT: 1000}]
    request = helpers.request.transfer(inputs, outputs)

    audit = nodes[0].ledgers[nodes[0].ledger_ids.index(3)]
    auditSizeOld = audit.size
    _, oldTxn = [txn for txn in audit.getAllTxn()][-1]

    reps = helpers.sdk.send_request_objects([request])
    helpers.sdk.sdk_get_and_check_replies(reps)
    assert auditSizeOld + 1 == audit.size
    _, newTxn = [txn for txn in audit.getAllTxn()][-1]
    assert oldTxn[TXN_PAYLOAD][TXN_PAYLOAD_DATA][AUDIT_TXN_LEDGERS_SIZE][1001] + 1 == \
           newTxn[TXN_PAYLOAD][TXN_PAYLOAD_DATA][AUDIT_TXN_LEDGERS_SIZE][1001]
    assert newTxn[TXN_PAYLOAD][TXN_PAYLOAD_DATA][AUDIT_TXN_LEDGER_ROOT][1001]
