        """Minimal Krea example: create one prediction and print the output URL(s)."""
        import krea_api

        output = krea_api.run({
    "prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light"
})
        print(output)
