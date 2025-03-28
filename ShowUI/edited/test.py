# from modeling_qwen2_vl import Qwen2VisionTransformerPretrainedModel, Qwen2VLForConditionalGeneration
# from transformers import Qwen2VLForConditionalGeneration, Qwen2VLProcessor
from modeling_qwen2_vl import Qwen2VLForConditionalGeneration
from processing_qwen2_vl import Qwen2VLProcessor
from configuration_qwen2_vl import Qwen2VLConfig
from qwen_vl_utils import process_vision_info
import time 

if __name__=="__main__":

    model_path = "/data/data1/syc/intern/wanshan/models/Qwen2-VL-2B-Instruct"
    device = 'cuda'
    uigraph_train = True        # Enable ui graph during training
    uigraph_test = True         # Enable ui graph during inference
    uigraph_diff = 1            # Pixel difference used for constructing ui graph
    uigraph_rand = False        # Enable random graph construction 
    # 2. Graph -> Mask 
    uimask_pre = True           # Prebuild patch selection mask in the preprocessor (not in model layers) for efficiency
    uimask_ratio = 0.5          # Specify the percentage of patch tokens to skip per component
    uimask_rand = False         # Enable random token selection instead of uniform selection
    processor = Qwen2VLProcessor.from_pretrained(
        model_path, 
    )
    messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "./chrome.png",
                # "resized_height": 28 * 30,
                # "resized_width": 28 * 30,
            },
            {"type": "text", "text": "Describe this image."},
        ],
    }
    ]
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to(device)
    
    # print(inputs)
    # print(inputs)
    # print(inputs['input_ids'].shape) # 
    # # print(inputs)
    # config = Qwen2VLConfig.from_pretrained(model_path)
    # print(config.vision_config)
    # vision_config = config.vision_config
    # vit = Qwen2VisionTransformerPretrainedModel(config.vision_config).to(device)
    # visual_tokens = vit(inputs['pixel_values'], grid_thw=inputs['image_grid_thw']) # TODO input['pixel_values'] shape is 2d tensor [seq_len, emb_dim] not 3d like in Qwen-VL [batch_size, seq_len, emb_dim]
    # print(visual_tokens.shape)

    # model = ShowUIForConditionalGeneration.from_pretrained(
    #     model_path,
    # ).to(device).eval()

    # start_time = time.time()
    # generated_ids = model.generate(**inputs, max_new_tokens=128)
    # elapsed_time = time.time() - start_time
    # print(f'elased_time : {elapsed_time}')
    # generated_ids_trimmed = [
    #     out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    # ]
    # output_text = processor.batch_decode(
    #     generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    # )
    # print(output_text)