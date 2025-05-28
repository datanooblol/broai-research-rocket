const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

export type GenerateEndpointType = 'generate-outline';
interface GenerateProps {
    endpoint: GenerateEndpointType;
    prompt: string;
}

export async function generateAPI({
    endpoint,
    prompt
}: GenerateProps) {    
    const body: Record<string, any> = {}
    if (endpoint === 'generate-outline') {
        body.instruction = prompt;
    }
    const res = await fetch(`${baseUrl}/v1/session/${endpoint}`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
    });
    
    if (!res.ok) {
        throw new Error(`Failed to generate content: ${res.statusText}`);
    }
    
    return res.json();
}