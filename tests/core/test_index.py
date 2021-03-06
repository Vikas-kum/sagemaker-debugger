# Standard Library
import json
import os
import shutil

# Third Party
import numpy as np

# First Party
from smdebug.core.locations import IndexFileLocationUtils, TensorFileLocation
from smdebug.core.reader import FileReader
from smdebug.core.writer import FileWriter


def test_index():
    numpy_tensor = [
        np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32),
        np.array([[1.0, 2.0, 4.0], [3.0, 4.0, 5.0]], dtype=np.float32),
    ]
    runid = "default"
    logdir = "."
    step = 0
    worker = "worker_0"
    run_dir = os.path.join(logdir, runid)
    writer = FileWriter(trial_dir=run_dir, step=step, worker=worker, verbose=True)
    for i in (0, len(numpy_tensor) - 1):
        n = "tensor" + str(i)
        writer.write_tensor(tdata=numpy_tensor[i], tname=n)
    writer.flush()
    writer.close()
    efl = TensorFileLocation(step_num=step, worker_name=worker)
    eventfile = efl.get_file_location(trial_dir=run_dir)
    indexfile = IndexFileLocationUtils.get_index_key_for_step(run_dir, step, worker)

    fo = open(eventfile, "rb")
    with open(indexfile) as idx_file:
        index_data = json.load(idx_file)
        tensor_payload = index_data["tensor_payload"]
        i = 0
        for tensor in tensor_payload:
            start_idx = int(tensor["start_idx"])
            fo.seek(start_idx, 0)
            length = int(tensor["length"])
            line = fo.read(length)
            zoo = open("test.txt", "wb")
            zoo.write(line)
            zoo.close()
            testfile_reader = FileReader("./test.txt")
            tensor_values = list(testfile_reader.read_tensors())
            assert np.allclose(
                tensor_values[0][2].all(), numpy_tensor[i].all()
            ), "indexwriter not working"
            i = i + 1

    fo.close()
    shutil.rmtree(run_dir)
    os.remove("test.txt")
