from datetime import datetime, timedelta
from types import SimpleNamespace

from models.preprocessing.timeseries_array import x_to_ts

cfg={
    'd_model':32,
    'n_heads':8,
    'batch_size':1,
    'seq_len':20
}
cfg = SimpleNamespace(**cfg)
import torch
import torch.nn as nn

from data.reader import Reader

data = torch.tensor(x_to_ts(Reader.get_pd("EURUSD", "M5",datetime.now()-timedelta(days=15))), dtype=torch.float32)
print(data.shape)
from models.Auto.layers import AutoCorrelation,AutoCorrelationLayer

class Model(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        auto_correlation = AutoCorrelation(
            factor= 1,
            attention_dropout=0.05,
            output_attention=True,
            scale=None,
            mask_flag=True)
        self.autocorr_layer = AutoCorrelationLayer(
            correlation=auto_correlation,
            d_model=cfg.d_model,
            n_heads=cfg.n_heads,
            d_keys=None
        )

    def forward(self, x, attn_mask=None):
        x=self.autocorr_layer(x,x,x,attn_mask)
        return x

model = Model(cfg)
out = model(data)
print(out)

