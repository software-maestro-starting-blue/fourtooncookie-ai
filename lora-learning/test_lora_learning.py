from lora_learning_script import learn_lora_model

def test1(): # learn_lora_model 구동 확인 테스트
    model_name = "test1"

    learn_lora_model(model_name,
                     epoch=1,
                     gradient_accumulation_steps=1,
                     train_batch_size=1,
                     learning_rate=0.0001,
                     text_encoder_lr=0.0001,
                     unet_lr=0.0001,
                     network_dim=8,
                     network_alpha=8,
                     rank_dropout=0,
                     module_dropout=0,
                     network_dropout=0,
                     optimizer_type="AdamW")
