from datetime import datetime, timedelta

from src.data.sources.utils import generate_batched_timestamps


def test_get_batched_timestamps():
    start = datetime(2020, 1, 1).timestamp()
    end = datetime(2020, 3, 5).timestamp()
    time_interval = 10
    expected_batches_length = 7
    batch_counter = 0
    for (start_timestamp, end_timestamp) in generate_batched_timestamps(
        start, end, time_interval
    ):
        batch_counter += 1
        assert start_timestamp == start
        start = (datetime.fromtimestamp(start) + timedelta(time_interval)).timestamp()
    

    assert end_timestamp == end
    assert batch_counter == expected_batches_length