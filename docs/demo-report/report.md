# BeamBench experiment report

> Generated from a validated tidy-results table. Statistical summaries are descriptive;
> this report does not claim significance or replace a preregistered analysis plan.

## Dataset

- Measurements: **216**
- Methods: **3**
- Metrics: **3**
- Conditions: **3**
- Baseline: **DAS**

![Experiment overview](overview.png)

## Aggregated results

| metric | method | condition | n | mean | std | sem | ci95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| localization_mae_deg | Binaural-PF | input SNR +0 dB | 8 | 13.91 | 1.42 | 0.5021 | 0.984 |
| localization_mae_deg | Binaural-PF | input SNR +5 dB | 8 | 10.88 | 0.95 | 0.3359 | 0.6583 |
| localization_mae_deg | Binaural-PF | input SNR -5 dB | 8 | 16.49 | 0.7832 | 0.2769 | 0.5428 |
| localization_mae_deg | DAS | input SNR +0 dB | 8 | 16.39 | 0.9946 | 0.3517 | 0.6892 |
| localization_mae_deg | DAS | input SNR +5 dB | 8 | 13.75 | 1.075 | 0.38 | 0.7447 |
| localization_mae_deg | DAS | input SNR -5 dB | 8 | 19.48 | 0.7244 | 0.2561 | 0.502 |
| localization_mae_deg | MVDR | input SNR +0 dB | 8 | 12.05 | 1.209 | 0.4275 | 0.8379 |
| localization_mae_deg | MVDR | input SNR +5 dB | 8 | 8.53 | 1.038 | 0.3671 | 0.7195 |
| localization_mae_deg | MVDR | input SNR -5 dB | 8 | 14.33 | 0.9488 | 0.3354 | 0.6575 |
| output_snr_db | Binaural-PF | input SNR +0 dB | 8 | 8.813 | 0.3298 | 0.1166 | 0.2286 |
| output_snr_db | Binaural-PF | input SNR +5 dB | 8 | 13.98 | 0.6404 | 0.2264 | 0.4438 |
| output_snr_db | Binaural-PF | input SNR -5 dB | 8 | 4.064 | 0.7693 | 0.272 | 0.5331 |
| output_snr_db | DAS | input SNR +0 dB | 8 | 6.793 | 0.5274 | 0.1865 | 0.3655 |
| output_snr_db | DAS | input SNR +5 dB | 8 | 11.23 | 0.5586 | 0.1975 | 0.3871 |
| output_snr_db | DAS | input SNR -5 dB | 8 | 1.319 | 0.7593 | 0.2685 | 0.5262 |
| output_snr_db | MVDR | input SNR +0 dB | 8 | 10.41 | 0.4337 | 0.1533 | 0.3006 |
| output_snr_db | MVDR | input SNR +5 dB | 8 | 15.46 | 0.4633 | 0.1638 | 0.321 |
| output_snr_db | MVDR | input SNR -5 dB | 8 | 5.496 | 0.4086 | 0.1445 | 0.2832 |

## Paired baseline comparison

Positive `delta_mean` means the candidate improved over the baseline. Direction is inferred
from common metric names and can be overridden through the Python API.

| metric | method | baseline | condition | pairs | delta_mean | delta_std | win_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| localization_mae_deg | Binaural-PF | DAS | input SNR +0 dB | 8 | 2.481 | 1.684 | 0.875 |
| localization_mae_deg | Binaural-PF | DAS | input SNR +5 dB | 8 | 2.874 | 1.304 | 1 |
| localization_mae_deg | Binaural-PF | DAS | input SNR -5 dB | 8 | 2.984 | 0.8898 | 1 |
| localization_mae_deg | MVDR | DAS | input SNR +0 dB | 8 | 4.34 | 1.249 | 1 |
| localization_mae_deg | MVDR | DAS | input SNR +5 dB | 8 | 5.22 | 1.483 | 1 |
| localization_mae_deg | MVDR | DAS | input SNR -5 dB | 8 | 5.149 | 1.543 | 1 |
| output_snr_db | Binaural-PF | DAS | input SNR +0 dB | 8 | 2.02 | 0.5411 | 1 |
| output_snr_db | Binaural-PF | DAS | input SNR +5 dB | 8 | 2.747 | 1.108 | 1 |
| output_snr_db | Binaural-PF | DAS | input SNR -5 dB | 8 | 2.744 | 1.181 | 1 |
| output_snr_db | MVDR | DAS | input SNR +0 dB | 8 | 3.614 | 0.6004 | 1 |
| output_snr_db | MVDR | DAS | input SNR +5 dB | 8 | 4.232 | 0.8313 | 1 |
| output_snr_db | MVDR | DAS | input SNR -5 dB | 8 | 4.176 | 0.9318 | 1 |
| runtime_ms | Binaural-PF | DAS | input SNR +0 dB | 8 | -0.8874 | 0.1137 | 0 |
| runtime_ms | Binaural-PF | DAS | input SNR +5 dB | 8 | -0.98 | 0.2826 | 0 |
| runtime_ms | Binaural-PF | DAS | input SNR -5 dB | 8 | -1.008 | 0.2656 | 0 |
| runtime_ms | MVDR | DAS | input SNR +0 dB | 8 | -1.647 | 0.2135 | 0 |
| runtime_ms | MVDR | DAS | input SNR +5 dB | 8 | -1.865 | 0.3212 | 0 |
| runtime_ms | MVDR | DAS | input SNR -5 dB | 8 | -1.767 | 0.3516 | 0 |

## Reproduce

```bash
beambench summarize path/to/results.csv --output report --baseline "DAS"
```
