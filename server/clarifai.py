from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2

from prompt import assist_prompt, classify_prompt


class ClarifaiService:
    def __init__(
        self,
        api_key: str,
        user_id: str,
        app_id: str,
        workflow_id: str,
    ):
        channel = ClarifaiChannel.get_grpc_channel()
        self.stub = service_pb2_grpc.V2Stub(channel)

        self.metadata = (('authorization', f'Key {api_key}'),)
        self.user_data = resources_pb2.UserAppIDSet(
            user_id=user_id, app_id=app_id)
        self.workflow_id = workflow_id

    def answer(
        self,
        user_input: str,
        faqs: list[tuple[str, str]],
        knowledge: list[str],
    ) -> str:
        raw_input = assist_prompt(
            faqs=faqs,
            knowledge=knowledge,
            query=user_input,
        )

        print(raw_input)

        input_to_model = resources_pb2.Input(
            data=resources_pb2.Data(
                text=resources_pb2.Text(
                    raw=raw_input,
                ),
            ),
        )
        request = service_pb2.PostWorkflowResultsRequest(
            user_app_id=self.user_data,
            workflow_id=self.workflow_id,
            inputs=[input_to_model],
        )

        response = self.stub.PostWorkflowResults(
            request,
            metadata=self.metadata,
        )

        if response.status.code != status_code_pb2.SUCCESS:
            print(response.status)
            raise Exception("Post workflow results failed, status: "
                            + response.status.description)

        result = response.results[0].outputs[0]

        return result.data.text.raw

    def classify(
        self,
        user_input: str,
        knowledge: list[tuple[str, str]],
    ) -> tuple[str, str]:
        input1, input2 = classify_prompt(
            knowledge=knowledge,
            query=user_input,
        )

        print(input1, "\n", input2)

        input_to_model1 = resources_pb2.Input(
            data=resources_pb2.Data(
                text=resources_pb2.Text(
                    raw=input1,
                ),
            ),
        )
        input_to_model2 = resources_pb2.Input(
            data=resources_pb2.Data(
                text=resources_pb2.Text(
                    raw=input2,
                ),
            ),
        )

        request1 = service_pb2.PostWorkflowResultsRequest(
            user_app_id=self.user_data,
            workflow_id=self.workflow_id,
            inputs=[input_to_model1],
        )
        request2 = service_pb2.PostWorkflowResultsRequest(
            user_app_id=self.user_data,
            workflow_id=self.workflow_id,
            inputs=[input_to_model2],
        )

        response1 = self.stub.PostWorkflowResults(
            request1,
            metadata=self.metadata,
        )
        response2 = self.stub.PostWorkflowResults(
            request2,
            metadata=self.metadata,
        )

        if [response1.status.code, response2.status.code] != [status_code_pb2.SUCCESS] * 2:
            print(response1.status)
            print(response2.status)
            raise Exception("Post workflow results failed, status: "
                            + response1.status.description
                            + ", "
                            + response2.status.description)

        result1 = response1.results[0].outputs[0]
        result2 = response2.results[0].outputs[0]

        # type, project
        return result1.data.text.raw, result2.data.text.raw
