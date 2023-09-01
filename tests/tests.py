import aoscx_handler
import pytest

def test_failed_login_raises_value_error():
    with pytest.raises(ValueError) as v_error:
        aoscx_handler.AoscxHandler('192.168.60.245', {'username':'admin','password':'admin'})