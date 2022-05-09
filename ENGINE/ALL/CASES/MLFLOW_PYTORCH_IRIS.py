import torch
import mlflow.pytorch
import os
import argparse
import tempfile
from tensorboardX import SummaryWriter
from ENGINE.ALL.MLFLOW_PYTORCH_IRIS import IrisClassifier, prepare_data, train_model, te

parser = argparse.ArgumentParser(description="PyTorch MNIST Example")
parser.add_argument(
    "--batch-size",
    type=int,
    default=64,
    metavar="N",
    help="input batch size for training (default: 64)",
)
parser.add_argument(
    "--test-batch-size",
    type=int,
    default=1000,
    metavar="N",
    help="input batch size for testing (default: 1000)",
)
parser.add_argument(
    "--epochs", type=int, default=10, metavar="N", help="number of epochs to train (default: 10)"
)
parser.add_argument(
    "--lr", type=float, default=0.01, metavar="LR", help="learning rate (default: 0.01)"
)
parser.add_argument(
    "--momentum", type=float, default=0.5, metavar="M", help="SGD momentum (default: 0.5)"
)
parser.add_argument(
    "--enable-cuda",
    type=str,
    choices=["True", "False"],
    default="True",
    help="enables or disables CUDA training",
)
parser.add_argument("--seed", type=int, default=1, metavar="S", help="random seed (default: 1)")
parser.add_argument(
    "--log-interval",
    type=int,
    default=100,
    metavar="N",
    help="how many batches to wait before logging training status",
)
args = parser.parse_args()

enable_cuda_flag = True if args.enable_cuda == "True" else False

args.cuda = enable_cuda_flag and torch.cuda.is_available()

torch.manual_seed(args.seed)
if args.cuda:
    torch.cuda.manual_seed(args.seed)

kwargs = {"num_workers": 1, "pin_memory": True} if args.cuda else {}

print(torch. __version__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = IrisClassifier()
model = model.to(device)
X_train, X_test, y_train, y_test, target_names = prepare_data()
model = train_model(model, 100, X_train, y_train)
te(model, X_test, y_test)

with mlflow.start_run() as run:
    # Log our parameters into mlflow
    for key, value in vars(args).items():
        mlflow.log_param(key, value)
    # Create a SummaryWriter to write TensorBoard events locally
    output_dir = dirpath = tempfile.mkdtemp()
    writer = SummaryWriter(output_dir)
    print("Writing TensorBoard events locally to %s\n" % output_dir)

    # Upload the TensorBoard event logs as a run artifact
    print("Uploading TensorBoard events as a run artifact...")
    mlflow.log_artifacts(output_dir, artifact_path="events")
    print(
        "\nLaunch TensorBoard with:\n\ntensorboard --logdir=%s"
        % os.path.join(mlflow.get_artifact_uri(), "events")
    )



    mlflow.pytorch.log_model(model, artifact_path="pytorch-model")
    print(
        "\nThe model is logged at:\n%s" % os.path.join(mlflow.get_artifact_uri(), "pytorch-model")
    )
    mlflow.pytorch.log_model(model, "model")  # logging scripted model
    model_path = mlflow.get_artifact_uri("model")
    loaded_pytorch_model = mlflow.pytorch.load_model(model_path)  # loading scripted model
    model.eval()
    with torch.no_grad():
        test_datapoint = torch.Tensor([4.4000, 3.0000, 1.3000, 0.2000]).to(device)
        prediction = loaded_pytorch_model(test_datapoint)
        actual = "setosa"
        predicted = target_names[torch.argmax(prediction)]
        print("\nPREDICTION RESULT: ACTUAL: {}, PREDICTED: {}".format(actual, predicted))