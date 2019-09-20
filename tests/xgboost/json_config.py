import json


def get_json_config(local_path):
    json_config = {
        "S3Path": "s3://kjndjknd_bucket/prefix",
        "LocalPath": local_path,
        "HookParameters": {
            "save_all": False,
            "save_steps": "0,1,2,3"
        }
    }

    return json.dumps(json_config)


def get_json_config_full(local_path):
    json_config = {
        "S3Path": "s3://kjndjknd_bucket/prefix",
        "LocalPath": local_path,
        "HookParameters": {
            "include_regex": "regexe1,regex2",
            "reductions": "min,max,mean,std,abs_variance,abs_sum,abs_l2_norm",
            "include_collections": "collection_obj_name1,collection_obj_name2",
            "save_all": False,
            "save_interval": 100,
            "save_steps": "1,2,3,4",
            "skip_num_steps": 1,
            "when_nan": "tensor1*,tensor2*"
        },
        "CollectionConfiguration": [
            {
                "CollectionName": "collection_obj_name1",
                "CollectionParameters": {
                    "include_regex": "regexe5*",
                    "save_interval": 100,
                    "save_steps": "1,2,3",
                    "skip_num_steps": 1,
                    "when_nan": "tensor3*,tensor4*",
                    "reductions": "min,abs_max,l1_norm,abs_l2_norm"
                }
            },
            {
                "CollectionName": "collection_obj_name2",
                "CollectionParameters": {
                    "include_regex": "regexe6*",
                    "save_interval": 100,
                    "save_steps": "1,2,3",
                    "skip_num_steps": 1,
                    "when_nan": "tensor3*,tensor4*",
                    "reductions": "min,abs_max,l1_norm,abs_l2_norm"
                }
            }
        ]
    }
    return json.dumps(json_config)