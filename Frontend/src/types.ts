/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface Agent {
  id: string;
  name: string;
  persona: string;
  thinking: {
    topic: string;
  };
  context: string[];
  response: string;
}

export interface Interaction {
  agentName: string;
  text: string;
}

export interface DefenseResult {
  userAttack: string;
  agentResponse: string;
}

export interface SimulationState {
  agents: Agent[];
  interactions: Interaction[];
  defense: DefenseResult | null;
}
